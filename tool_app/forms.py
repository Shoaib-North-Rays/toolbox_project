from django import forms
from .models import FileConversion


class FileUploadForm(forms.ModelForm):
    """Form for uploading files for conversion"""
    
    class Meta:
        model = FileConversion
        fields = ['original_file', 'conversion_type']
        widgets = {
            'original_file': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer',
                'accept': '.txt,.pdf,.doc,.docx'
            }),
            'conversion_type': forms.Select(attrs={
                'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['original_file'].label = 'Select File'
        self.fields['conversion_type'].label = 'Conversion Type'
        self.fields['original_file'].help_text = 'Supported formats: TXT, PDF, DOC, DOCX'
    
    def clean_original_file(self):
        file = self.cleaned_data.get('original_file')
        if file:
            # Check file size (10MB limit)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('File size cannot exceed 10MB')
            
            # Check file extension
            allowed_extensions = ['.txt', '.pdf', '.doc', '.docx']
            file_extension = '.' + file.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise forms.ValidationError('Unsupported file format. Please upload TXT, PDF, DOC, or DOCX files only.')
        
        return file


class TextToPdfForm(forms.Form):
    """Form for converting text to PDF"""
    text_content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'rows': 10,
            'placeholder': 'Enter your text here...'
        }),
        label='Text Content',
        help_text='Enter the text you want to convert to PDF'
    )
    
    title = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Document title (optional)'
        }),
        label='Document Title'
    )