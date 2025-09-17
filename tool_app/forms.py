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


class ImageUploadForm(forms.ModelForm):
    """Form for uploading images for processing"""
    
    class Meta:
        model = FileConversion
        fields = ['original_file', 'conversion_type']
        widgets = {
            'original_file': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer',
                'accept': '.jpg,.jpeg,.png,.gif,.bmp,.webp,.tiff'
            }),
            'conversion_type': forms.Select(attrs={
                'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter conversion types for image operations
        self.fields['conversion_type'].choices = [
            ('image_compress', 'Image Compression'),
            ('image_convert', 'Image Format Conversion'),
        ]
        self.fields['original_file'].label = 'Select Image'
        self.fields['conversion_type'].label = 'Operation Type'
        self.fields['original_file'].help_text = 'Supported formats: JPG, PNG, GIF, BMP, WebP, TIFF'
    
    def clean_original_file(self):
        file = self.cleaned_data.get('original_file')
        if file:
            # Check file size (20MB limit for images)
            if file.size > 20 * 1024 * 1024:
                raise forms.ValidationError('Image size cannot exceed 20MB')
            
            # Check file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']
            file_extension = '.' + file.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise forms.ValidationError('Unsupported image format. Please upload JPG, PNG, GIF, BMP, WebP, or TIFF files only.')
        
        return file


class ImageCompressionForm(forms.Form):
    """Form for image compression settings"""
    image_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer',
            'accept': '.jpg,.jpeg,.png,.gif,.bmp,.webp,.tiff'
        }),
        label='Select Image',
        help_text='Supported formats: JPG, PNG, GIF, BMP, WebP, TIFF'
    )
    
    quality = forms.IntegerField(
        min_value=10,
        max_value=95,
        initial=80,
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'type': 'range'
        }),
        label='Compression Quality (%)',
        help_text='Lower values = smaller file size, lower quality (10-95)'
    )
    
    resize_width = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=5000,
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Leave empty to keep original width'
        }),
        label='Resize Width (optional)',
        help_text='Resize image width in pixels (height will be adjusted proportionally)'
    )


class ImageConversionForm(forms.Form):
    """Form for image format conversion"""
    image_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer',
            'accept': '.jpg,.jpeg,.png,.gif,.bmp,.webp,.tiff'
        }),
        label='Select Image',
        help_text='Supported formats: JPG, PNG, GIF, BMP, WebP, TIFF'
    )
    
    target_format = forms.ChoiceField(
        choices=[
            ('JPEG', 'JPEG'),
            ('PNG', 'PNG'),
            ('WEBP', 'WebP'),
            ('BMP', 'BMP'),
            ('TIFF', 'TIFF'),
        ],
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='Target Format'
    )
    
    quality = forms.IntegerField(
        min_value=10,
        max_value=95,
        initial=85,
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'type': 'range'
        }),
        label='Quality (%)',
        help_text='Only applies to JPEG and WebP formats'
    )


class QRCodeForm(forms.Form):
    """Form for QR code generation"""
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'rows': 4,
            'placeholder': 'Enter text, URL, or data for QR code...'
        }),
        label='QR Code Content',
        help_text='Text, URL, or data to encode in the QR code'
    )
    
    size = forms.ChoiceField(
        choices=[
            ('small', 'Small (200x200)'),
            ('medium', 'Medium (400x400)'),
            ('large', 'Large (600x600)'),
            ('xlarge', 'Extra Large (800x800)'),
        ],
        initial='medium',
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='QR Code Size'
    )
    
    format = forms.ChoiceField(
        choices=[
            ('PNG', 'PNG'),
            ('JPEG', 'JPEG'),
            ('SVG', 'SVG (Vector)'),
        ],
        initial='PNG',
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='Output Format'
    )


class MetaTagForm(forms.Form):
    """Form for meta tag generation"""
    title = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter page title (recommended: 50-60 characters)'
        }),
        label='Page Title',
        help_text='The title that appears in search results and browser tabs'
    )
    
    description = forms.CharField(
        max_length=160,
        widget=forms.Textarea(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'rows': 3,
            'placeholder': 'Enter meta description (recommended: 150-160 characters)'
        }),
        label='Meta Description',
        help_text='Brief description that appears in search results'
    )
    
    keywords = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'keyword1, keyword2, keyword3'
        }),
        label='Keywords (Optional)',
        help_text='Comma-separated keywords (not heavily weighted by search engines)'
    )
    
    author = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Author name'
        }),
        label='Author (Optional)',
        help_text='Content author or website owner'
    )
    
    canonical_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'https://example.com/page'
        }),
        label='Canonical URL (Optional)',
        help_text='Preferred URL for this content to avoid duplicate content issues'
    )
    
    og_image = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'https://example.com/image.jpg'
        }),
        label='Open Graph Image (Optional)',
        help_text='Image URL for social media sharing (recommended: 1200x630px)'
    )


class URLEncoderDecoderForm(forms.Form):
    """Form for URL encoding and decoding"""
    url_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'rows': 4,
            'placeholder': 'Enter URL or text to encode/decode...'
        }),
        label='URL or Text',
        help_text='Enter the URL or text you want to encode or decode'
    )
    
    operation = forms.ChoiceField(
        choices=[
            ('encode', 'URL Encode'),
            ('decode', 'URL Decode'),
        ],
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='Operation'
    )


class DomainResolverForm(forms.Form):
    """Form for domain to IP resolution"""
    domain = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'example.com'
        }),
        label='Domain Name',
        help_text='Enter domain name without http:// or https://'
    )
    
    record_type = forms.ChoiceField(
        choices=[
            ('A', 'A - IPv4 Address'),
            ('AAAA', 'AAAA - IPv6 Address'),
            ('CNAME', 'CNAME - Canonical Name'),
            ('MX', 'MX - Mail Exchange'),
            ('NS', 'NS - Name Servers'),
            ('TXT', 'TXT - Text Records'),
        ],
        initial='A',
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='DNS Record Type'
    )


class WhoisLookupForm(forms.Form):
    """Form for Whois lookup"""
    domain = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'example.com'
        }),
        label='Domain Name',
        help_text='Enter domain name without http:// or https://'
    )


class RobotsSitemapForm(forms.Form):
    """Form for robots.txt and sitemap.xml generation"""
    domain_url = forms.URLField(
        widget=forms.URLInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'https://example.com'
        }),
        label='Website URL',
        help_text='Full URL of your website including https://'
    )
    
    sitemap_urls = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'rows': 8,
            'placeholder': 'https://example.com/\nhttps://example.com/about\nhttps://example.com/contact\nhttps://example.com/products'
        }),
        label='Sitemap URLs',
        help_text='Enter one URL per line for your sitemap.xml'
    )
    
    disallow_paths = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'rows': 4,
            'placeholder': '/admin/\n/private/\n/temp/'
        }),
        label='Disallow Paths (Optional)',
        help_text='Enter paths to disallow in robots.txt (one per line, starting with /)'
    )
    
    crawl_delay = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=86400,
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': '1'
        }),
        label='Crawl Delay (Optional)',
        help_text='Delay in seconds between crawler requests'
    )


# Security & Utility Tools Forms

class HashGeneratorForm(forms.Form):
    """Form for hash generation"""
    text_input = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'rows': 4,
            'placeholder': 'Enter text to hash...'
        }),
        label='Text to Hash',
        help_text='Enter the text you want to generate hashes for'
    )
    
    hash_types = forms.MultipleChoiceField(
        choices=[
            ('md5', 'MD5'),
            ('sha1', 'SHA1'),
            ('sha256', 'SHA256'),
            ('sha512', 'SHA512'),
            ('sha224', 'SHA224'),
            ('sha384', 'SHA384'),
        ],
        initial=['md5', 'sha1', 'sha256'],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-checkbox'
        }),
        label='Hash Types',
        help_text='Select which hash algorithms to generate'
    )


class JWTDecoderForm(forms.Form):
    """Form for JWT token decoding"""
    jwt_token = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'rows': 4,
            'placeholder': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
        }),
        label='JWT Token',
        help_text='Enter the JWT token to decode (paste the complete token)'
    )


class SSLCheckerForm(forms.Form):
    """Form for SSL certificate checking"""
    domain = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'example.com'
        }),
        label='Domain Name',
        help_text='Enter domain name without https:// (e.g., google.com)'
    )
    
    port = forms.IntegerField(
        initial=443,
        min_value=1,
        max_value=65535,
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='Port',
        help_text='SSL port number (default: 443)'
    )


class EmailValidatorForm(forms.Form):
    """Form for email validation"""
    email_list = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'rows': 6,
            'placeholder': 'user@example.com\nanother@domain.org\ninvalid.email'
        }),
        label='Email Addresses',
        help_text='Enter email addresses (one per line) to validate'
    )
    
    check_mx = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox'
        }),
        label='Check MX Records',
        help_text='Verify that the domain has valid mail exchange records'
    )


class TextEncryptionForm(forms.Form):
    """Form for text encryption/decryption"""
    operation = forms.ChoiceField(
        choices=[
            ('encrypt', 'Encrypt'),
            ('decrypt', 'Decrypt'),
        ],
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='Operation'
    )
    
    algorithm = forms.ChoiceField(
        choices=[
            ('base64', 'Base64 Encoding'),
            ('caesar', 'Caesar Cipher'),
            ('rot13', 'ROT13'),
        ],
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='Algorithm'
    )
    
    text_input = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'rows': 4,
            'placeholder': 'Enter text to encrypt/decrypt...'
        }),
        label='Text Input',
        help_text='Enter the text to encrypt or decrypt'
    )
    
    key = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=25,
        initial=3,
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='Caesar Cipher Key (Optional)',
        help_text='Shift value for Caesar cipher (1-25, only applies to Caesar cipher)'
    )


# Fun & Engagement Tools Forms

class MemeGeneratorForm(forms.Form):
    """Form for meme generation"""
    image_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer',
            'accept': '.jpg,.jpeg,.png,.gif,.bmp,.webp'
        }),
        label='Upload Image',
        help_text='Supported formats: JPG, PNG, GIF, BMP, WebP (max 10MB)'
    )
    
    top_text = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Top text (optional)'
        }),
        label='Top Text',
        help_text='Text to display at the top of the image'
    )
    
    bottom_text = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Bottom text (optional)'
        }),
        label='Bottom Text',
        help_text='Text to display at the bottom of the image'
    )
    
    font_size = forms.IntegerField(
        initial=40,
        min_value=20,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'type': 'range'
        }),
        label='Font Size',
        help_text='Size of the text (20-100)'
    )


class EmojiTranslatorForm(forms.Form):
    """Form for emoji translation"""
    text_input = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'rows': 4,
            'placeholder': 'Enter text to translate to emojis...'
        }),
        label='Text to Translate',
        help_text='Enter text and we\'ll add relevant emojis'
    )
    
    translation_mode = forms.ChoiceField(
        choices=[
            ('replace', 'Replace words with emojis'),
            ('append', 'Add emojis after words'),
            ('prepend', 'Add emojis before words'),
        ],
        initial='append',
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='Translation Mode'
    )


class RandomQuoteForm(forms.Form):
    """Form for random quote generation"""
    category = forms.ChoiceField(
        choices=[
            ('all', 'All Categories'),
            ('inspirational', 'Inspirational'),
            ('motivational', 'Motivational'),
            ('funny', 'Funny'),
            ('love', 'Love'),
            ('life', 'Life'),
            ('success', 'Success'),
            ('wisdom', 'Wisdom'),
        ],
        initial='all',
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='Quote Category'
    )
    
    count = forms.IntegerField(
        initial=1,
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='Number of Quotes',
        help_text='How many quotes to generate (1-10)'
    )


class RandomNameForm(forms.Form):
    """Form for random name generation"""
    name_type = forms.ChoiceField(
        choices=[
            ('full', 'Full Name (First + Last)'),
            ('first', 'First Name Only'),
            ('last', 'Last Name Only'),
            ('username', 'Username'),
        ],
        initial='full',
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='Name Type'
    )
    
    gender = forms.ChoiceField(
        choices=[
            ('any', 'Any Gender'),
            ('male', 'Male'),
            ('female', 'Female'),
        ],
        initial='any',
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='Gender Preference'
    )
    
    count = forms.IntegerField(
        initial=5,
        min_value=1,
        max_value=20,
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='Number of Names',
        help_text='How many names to generate (1-20)'
    )


class UnitConverterForm(forms.Form):
    """Form for unit conversion"""
    conversion_type = forms.ChoiceField(
        choices=[
            ('length', 'Length/Distance'),
            ('weight', 'Weight/Mass'),
            ('temperature', 'Temperature'),
            ('volume', 'Volume'),
            ('area', 'Area'),
            ('speed', 'Speed'),
        ],
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='Conversion Type'
    )
    
    value = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'step': 'any',
            'placeholder': '0'
        }),
        label='Value to Convert'
    )
    
    from_unit = forms.CharField(
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='From Unit'
    )
    
    to_unit = forms.CharField(
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='To Unit'
    )


# Audio/Video Tools Forms

class AudioConverterForm(forms.Form):
    """Form for audio format conversion"""
    audio_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer',
            'accept': '.mp3,.wav,.flac,.aac,.ogg,.m4a,.wma'
        }),
        label='Upload Audio File',
        help_text='Supported formats: MP3, WAV, FLAC, AAC, OGG, M4A, WMA (max 50MB)'
    )
    
    target_format = forms.ChoiceField(
        choices=[
            ('mp3', 'MP3'),
            ('wav', 'WAV'),
            ('flac', 'FLAC'),
            ('aac', 'AAC'),
            ('ogg', 'OGG'),
            ('m4a', 'M4A'),
        ],
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='Target Format'
    )
    
    quality = forms.ChoiceField(
        choices=[
            ('128', 'Standard (128 kbps)'),
            ('192', 'Good (192 kbps)'),
            ('256', 'High (256 kbps)'),
            ('320', 'Very High (320 kbps)'),
        ],
        initial='192',
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='Audio Quality'
    )
    
    def clean_audio_file(self):
        file = self.cleaned_data.get('audio_file')
        if file:
            # Check file size (50MB limit)
            if file.size > 50 * 1024 * 1024:
                raise forms.ValidationError('Audio file size cannot exceed 50MB')
            
            # Check file extension
            allowed_extensions = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma']
            file_extension = '.' + file.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise forms.ValidationError('Unsupported audio format. Please upload MP3, WAV, FLAC, AAC, OGG, M4A, or WMA files only.')
        
        return file


class AudioSpeedChangerForm(forms.Form):
    """Form for changing audio playback speed"""
    audio_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer',
            'accept': '.mp3,.wav,.flac,.aac,.ogg,.m4a'
        }),
        label='Upload Audio File',
        help_text='Supported formats: MP3, WAV, FLAC, AAC, OGG, M4A (max 50MB)'
    )
    
    speed_multiplier = forms.FloatField(
        initial=1.0,
        min_value=0.25,
        max_value=4.0,
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'step': '0.1',
            'placeholder': '1.0'
        }),
        label='Speed Multiplier',
        help_text='0.25 = 4x slower, 1.0 = normal speed, 2.0 = 2x faster, 4.0 = 4x faster'
    )
    
    preserve_pitch = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox'
        }),
        label='Preserve Pitch',
        help_text='Keep the original pitch when changing speed (prevents chipmunk effect)'
    )
    
    output_format = forms.ChoiceField(
        choices=[
            ('mp3', 'MP3'),
            ('wav', 'WAV'),
            ('flac', 'FLAC'),
            ('aac', 'AAC'),
        ],
        initial='mp3',
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='Output Format'
    )
    
    def clean_audio_file(self):
        file = self.cleaned_data.get('audio_file')
        if file:
            # Check file size (50MB limit)
            if file.size > 50 * 1024 * 1024:
                raise forms.ValidationError('Audio file size cannot exceed 50MB')
        
        return file


class VideoToAudioForm(forms.Form):
    """Form for extracting audio from video files"""
    video_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer',
            'accept': '.mp4,.avi,.mov,.mkv,.wmv,.flv,.webm,.m4v'
        }),
        label='Upload Video File',
        help_text='Supported formats: MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V (max 100MB)'
    )
    
    audio_format = forms.ChoiceField(
        choices=[
            ('mp3', 'MP3'),
            ('wav', 'WAV'),
            ('flac', 'FLAC'),
            ('aac', 'AAC'),
            ('ogg', 'OGG'),
        ],
        initial='mp3',
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='Audio Format'
    )
    
    audio_quality = forms.ChoiceField(
        choices=[
            ('128', 'Standard (128 kbps)'),
            ('192', 'Good (192 kbps)'),
            ('256', 'High (256 kbps)'),
            ('320', 'Very High (320 kbps)'),
        ],
        initial='192',
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label='Audio Quality'
    )
    
    start_time = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': '00:00:00 (optional)'
        }),
        label='Start Time (Optional)',
        help_text='Format: HH:MM:SS or MM:SS (e.g., 01:30 or 00:01:30)'
    )
    
    end_time = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': '00:00:00 (optional)'
        }),
        label='End Time (Optional)',
        help_text='Format: HH:MM:SS or MM:SS (e.g., 03:45 or 00:03:45)'
    )
    
    def clean_video_file(self):
        file = self.cleaned_data.get('video_file')
        if file:
            # Check file size (100MB limit)
            if file.size > 100 * 1024 * 1024:
                raise forms.ValidationError('Video file size cannot exceed 100MB')
            
            # Check file extension
            allowed_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v']
            file_extension = '.' + file.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise forms.ValidationError('Unsupported video format. Please upload MP4, AVI, MOV, MKV, WMV, FLV, WebM, or M4V files only.')
        
        return file
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        # Validate time format if provided
        if start_time:
            try:
                self._parse_time(start_time)
            except ValueError:
                raise forms.ValidationError({'start_time': 'Invalid time format. Use HH:MM:SS or MM:SS.'})
        
        if end_time:
            try:
                self._parse_time(end_time)
            except ValueError:
                raise forms.ValidationError({'end_time': 'Invalid time format. Use HH:MM:SS or MM:SS.'})
        
        return cleaned_data
    
    def _parse_time(self, time_str):
        """Parse time string to seconds"""
        parts = time_str.split(':')
        if len(parts) == 2:  # MM:SS
            minutes, seconds = map(int, parts)
            return minutes * 60 + seconds
        elif len(parts) == 3:  # HH:MM:SS
            hours, minutes, seconds = map(int, parts)
            return hours * 3600 + minutes * 60 + seconds
        else:
            raise ValueError('Invalid time format')
