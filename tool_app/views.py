import os
import tempfile
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, FileResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
import json
from docx import Document
from docx.shared import Inches

from .models import FileConversion
from .forms import FileUploadForm, TextToPdfForm


def home(request):
    """Home page with tool overview"""
    return render(request, 'tool_app/home.html')


def file_converter(request):
    """File converter tool page"""
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            conversion = form.save(commit=False)
            conversion.status = 'processing'
            conversion.save()
            
            # Process the conversion
            try:
                converted_file = process_file_conversion(conversion)
                if converted_file:
                    conversion.converted_file = converted_file
                    conversion.status = 'completed'
                    conversion.save()
                    messages.success(request, 'File converted successfully!')
                    return redirect('tool_app:conversion_result', pk=conversion.pk)
                else:
                    conversion.status = 'failed'
                    conversion.error_message = 'Conversion failed'
                    conversion.save()
                    messages.error(request, 'File conversion failed. Please try again.')
            except Exception as e:
                conversion.status = 'failed'
                conversion.error_message = str(e)
                conversion.save()
                messages.error(request, f'Error during conversion: {str(e)}')
    else:
        form = FileUploadForm()
    
    return render(request, 'tool_app/file_converter.html', {'form': form})


def text_to_pdf(request):
    """Text to PDF converter"""
    if request.method == 'POST':
        form = TextToPdfForm(request.POST)
        if form.is_valid():
            try:
                pdf_buffer = create_pdf_from_text(
                    form.cleaned_data['text_content'],
                    form.cleaned_data.get('title', 'Document')
                )
                
                response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="converted_document.pdf"'
                return response
            except Exception as e:
                messages.error(request, f'Error creating PDF: {str(e)}')
    else:
        form = TextToPdfForm()
    
    return render(request, 'tool_app/text_to_pdf.html', {'form': form})


def conversion_result(request, pk):
    """Display conversion result"""
    conversion = get_object_or_404(FileConversion, pk=pk)
    return render(request, 'tool_app/conversion_result.html', {'conversion': conversion})


def download_file(request, pk):
    """Download converted file"""
    conversion = get_object_or_404(FileConversion, pk=pk)
    if conversion.converted_file:
        response = FileResponse(
            conversion.converted_file.open(),
            as_attachment=True,
            filename=conversion.converted_filename
        )
        return response
    else:
        messages.error(request, 'File not found or conversion not completed.')
        return redirect('tool_app:home')


# JSON API Views
@csrf_exempt
@require_POST
def api_convert_file(request):
    """API endpoint for file conversion"""
    try:
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)
        
        file = request.FILES['file']
        conversion_type = request.POST.get('conversion_type')
        
        if not conversion_type:
            return JsonResponse({'error': 'No conversion type specified'}, status=400)
        
        # Create conversion record
        conversion = FileConversion.objects.create(
            original_file=file,
            conversion_type=conversion_type,
            status='processing'
        )
        
        # Process conversion
        converted_file = process_file_conversion(conversion)
        
        if converted_file:
            conversion.converted_file = converted_file
            conversion.status = 'completed'
            conversion.save()
            
            return JsonResponse({
                'success': True,
                'conversion_id': conversion.id,
                'download_url': f'/download/{conversion.id}/',
                'original_filename': conversion.original_filename,
                'converted_filename': conversion.converted_filename
            })
        else:
            conversion.status = 'failed'
            conversion.save()
            return JsonResponse({'error': 'Conversion failed'}, status=500)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def api_text_to_pdf(request):
    """API endpoint for text to PDF conversion"""
    try:
        data = json.loads(request.body)
        text_content = data.get('text_content')
        title = data.get('title', 'Document')
        
        if not text_content:
            return JsonResponse({'error': 'No text content provided'}, status=400)
        
        pdf_buffer = create_pdf_from_text(text_content, title)
        
        # Return base64 encoded PDF
        import base64
        pdf_base64 = base64.b64encode(pdf_buffer.getvalue()).decode('utf-8')
        
        return JsonResponse({
            'success': True,
            'pdf_data': pdf_base64,
            'filename': f'{title.replace(" ", "_")}.pdf'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def api_conversion_status(request, pk):
    """API endpoint to check conversion status"""
    try:
        conversion = get_object_or_404(FileConversion, pk=pk)
        return JsonResponse({
            'id': conversion.id,
            'status': conversion.status,
            'conversion_type': conversion.conversion_type,
            'original_filename': conversion.original_filename,
            'converted_filename': conversion.converted_filename,
            'created_at': conversion.created_at.isoformat(),
            'error_message': conversion.error_message
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Helper functions
def process_file_conversion(conversion):
    """Process file conversion based on type"""
    try:
        if conversion.conversion_type == 'txt_to_pdf':
            return convert_txt_to_pdf(conversion.original_file)
        elif conversion.conversion_type == 'pdf_to_txt':
            return convert_pdf_to_txt(conversion.original_file)
        elif conversion.conversion_type == 'doc_to_pdf':
            return convert_doc_to_pdf(conversion.original_file)
        elif conversion.conversion_type == 'pdf_to_doc':
            return convert_pdf_to_doc(conversion.original_file)
        else:
            raise ValueError(f"Unsupported conversion type: {conversion.conversion_type}")
    except Exception as e:
        print(f"Conversion error: {e}")
        return None


def convert_txt_to_pdf(txt_file):
    """Convert text file to PDF"""
    try:
        # Read text content
        content = txt_file.read().decode('utf-8')
        
        # Create PDF
        pdf_buffer = create_pdf_from_text(content, "Converted Document")
        
        # Save to file
        filename = f"converted_{txt_file.name.split('.')[0]}.pdf"
        return ContentFile(pdf_buffer.getvalue(), name=filename)
        
    except Exception as e:
        print(f"TXT to PDF conversion error: {e}")
        return None


def convert_pdf_to_txt(pdf_file):
    """Convert PDF to text file"""
    try:
        # This is a simplified implementation
        # For production, you'd use PyPDF2 or pdfplumber
        content = "PDF to text conversion is not fully implemented in this demo.\nThis would require additional libraries like PyPDF2 or pdfplumber."
        
        filename = f"converted_{pdf_file.name.split('.')[0]}.txt"
        return ContentFile(content.encode('utf-8'), name=filename)
        
    except Exception as e:
        print(f"PDF to TXT conversion error: {e}")
        return None


def convert_doc_to_pdf(doc_file):
    """Convert DOC/DOCX to PDF"""
    try:
        # Read DOCX content
        doc = Document(doc_file)
        content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        # Convert to PDF
        pdf_buffer = create_pdf_from_text(content, "Converted Document")
        
        filename = f"converted_{doc_file.name.split('.')[0]}.pdf"
        return ContentFile(pdf_buffer.getvalue(), name=filename)
        
    except Exception as e:
        print(f"DOC to PDF conversion error: {e}")
        return None


def convert_pdf_to_doc(pdf_file):
    """Convert PDF to DOC/DOCX"""
    try:
        # This is a simplified implementation
        content = "PDF to DOC conversion is not fully implemented in this demo.\nThis would require additional libraries for PDF parsing."
        
        # Create DOCX
        doc = Document()
        doc.add_paragraph(content)
        
        # Save to buffer
        doc_buffer = BytesIO()
        doc.save(doc_buffer)
        doc_buffer.seek(0)
        
        filename = f"converted_{pdf_file.name.split('.')[0]}.docx"
        return ContentFile(doc_buffer.getvalue(), name=filename)
        
    except Exception as e:
        print(f"PDF to DOC conversion error: {e}")
        return None


def create_pdf_from_text(text_content, title):
    """Create PDF from text content"""
    buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Add title
    story.append(Paragraph(title, styles['Title']))
    
    # Add content
    for line in text_content.split('\n'):
        if line.strip():
            story.append(Paragraph(line, styles['Normal']))
        else:
            story.append(Paragraph('<br/>', styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer
