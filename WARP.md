# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a production-ready Django web application providing online file conversion and image processing tools. It uses Django MVT (Model-View-Template) architecture with Tailwind CSS for styling.

### Tech Stack
- **Backend**: Django 4.2.7
- **Frontend**: Tailwind CSS (via CDN)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Image Processing**: Pillow (PIL Fork)
- **QR Code Generation**: qrcode library
- **Document Processing**: ReportLab (PDF), python-docx (Word documents)
- **Web & SEO Tools**: DNS resolution (dnspython), domain lookups (python-whois)
- **Networking**: HTTP requests, URL encoding/decoding

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Database Operations
```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Check for issues
python manage.py check

# Reset database (development only)
python manage.py flush
```

### Development Server
```bash
# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8080

# Run with specific IP and port
python manage.py runserver 0.0.0.0:8000
```

### Testing and Debugging
```bash
# Run tests
python manage.py test

# Run tests for specific app
python manage.py test tool_app

# Django shell for debugging
python manage.py shell

# Collect static files (production)
python manage.py collectstatic
```

## Project Architecture

### Directory Structure
```
toolbox_project/
├── toolbox_project/          # Django project settings
│   ├── settings.py           # Main configuration
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py              # WSGI configuration
├── tool_app/                # Main application
│   ├── models.py            # Data models (FileConversion)
│   ├── views.py             # Business logic and request handling
│   ├── forms.py             # Django forms for user input
│   ├── urls.py              # App-specific URL routing
│   ├── templates/tool_app/  # HTML templates
│   └── migrations/          # Database migrations
├── templates/               # Global templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # Uploaded and processed files
└── requirements.txt         # Python dependencies
```

### Core Models

**FileConversion Model** (`tool_app/models.py`)
- Tracks all file conversions and image processing operations
- Supported conversion types:
  - `txt_to_pdf`, `pdf_to_txt`, `doc_to_pdf`, `pdf_to_doc`
  - `image_compress`, `image_convert`, `qr_generate`
- Status tracking: pending → processing → completed/failed
- Automatic file organization by date (`uploads/YYYY/MM/DD/`)

### Application Flow

1. **Request Handling**: URLs route to views in `tool_app/views.py`
2. **Form Processing**: Django forms validate user input
3. **File Processing**: Helper functions handle conversions/processing
4. **Response**: Direct download or redirect to result page
5. **Storage**: Files stored in `media/uploads/` with date-based organization

### Available Tools

#### Document Processing
- **File Converter** (`/file-converter/`): Convert between TXT, PDF, DOC, DOCX
- **Text to PDF** (`/text-to-pdf/`): Convert plain text to formatted PDF

#### Image Processing
- **Image Compression** (`/image-compression/`): Reduce file sizes with quality control
- **Image Conversion** (`/image-conversion/`): Convert between JPG, PNG, WebP, BMP, TIFF
- **QR Code Generator** (`/qr-code-generator/`): Generate QR codes in multiple formats

#### Web & SEO Tools
- **Meta Tag Generator** (`/meta-tag-generator/`): Generate SEO-optimized HTML meta tags
- **URL Encoder/Decoder** (`/url-encoder-decoder/`): Encode/decode URLs for safe transmission
- **Domain IP Resolver** (`/domain-ip-resolver/`): Resolve domains to IPs and DNS records
- **Whois Lookup** (`/whois-lookup/`): Get domain registration information
- **Robots.txt & Sitemap Generator** (`/robots-sitemap-generator/`): Generate SEO files

#### API Endpoints
- `POST /api/convert/` - File conversion API
- `POST /api/text-to-pdf/` - Text to PDF conversion
- `GET /api/status/<id>/` - Conversion status check

## Development Guidelines

### Adding New Tools

1. **Update Models**: Add new conversion types to `CONVERSION_TYPES` in `models.py`
2. **Create Forms**: Add form classes in `forms.py` with proper validation
3. **Implement Views**: Add view functions in `views.py` with helper functions
4. **Add URLs**: Register new URL patterns in `tool_app/urls.py`
5. **Create Templates**: Build HTML templates following existing patterns
6. **Update Navigation**: Add tool to home page (`templates/tool_app/home.html`)

### File Processing Pattern

All file processing follows this pattern:
```python
def process_function(file, **options):
    """Process file and return BytesIO buffer"""
    try:
        # Open and process file
        result = process_file(file)
        
        # Create buffer
        buffer = BytesIO()
        result.save(buffer, format='FORMAT')
        buffer.seek(0)
        
        return buffer
    except Exception as e:
        print(f"Processing error: {e}")
        return None
```

### Form Validation Standards

- File size limits: 10MB for documents, 20MB for images
- Supported extensions validation in `clean_*` methods
- Consistent error messaging and help text
- Tailwind CSS classes for styling

### Template Structure

All templates extend `base.html` and follow this structure:
- Header with tool icon and description
- Main form with proper error handling
- Feature/information sections
- Consistent styling with tool-specific colors

### File Storage

- **Upload Path**: `media/uploads/YYYY/MM/DD/filename`
- **Generated by**: `upload_to_files()` function in models
- **Cleanup**: Implement cleanup for old files in production

### Image Processing Specifics

- **Library**: PIL/Pillow for image operations
- **Formats**: JPEG, PNG, GIF, BMP, WebP, TIFF support
- **Quality Control**: Adjustable compression (10-95%)
- **Resizing**: Proportional scaling with width specification
- **Color Mode**: Automatic RGB conversion for JPEG compatibility

### QR Code Generation

- **Library**: qrcode with optional SVG support
- **Sizes**: 200x200 to 800x800 pixels
- **Formats**: PNG, JPEG, SVG output
- **Error Correction**: Level L (Low) for maximum data capacity

### Web & SEO Tools Specifics

- **DNS Resolution**: Uses dnspython for reliable DNS queries
- **Whois Lookups**: python-whois library for domain information
- **URL Processing**: Built-in urllib.parse for encoding/decoding
- **Meta Tag Generation**: Comprehensive SEO tag creation
- **XML Generation**: ElementTree for sitemap.xml creation
- **Error Handling**: Graceful handling of network timeouts and failures

## Production Considerations

### Environment Variables
```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/dbname
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Static Files
```bash
# Set in production settings
STATIC_ROOT = '/path/to/static/'
MEDIA_ROOT = '/path/to/media/'

# Collect static files
python manage.py collectstatic --noinput
```

### Database
- SQLite for development
- PostgreSQL recommended for production
- Regular backups for conversion history

### Security
- File type validation in forms
- File size limits enforced
- No direct file execution
- Secure file storage with proper permissions

## Debugging Tips

### Common Issues

**Import Errors**: Ensure all dependencies in requirements.txt are installed
```bash
pip install -r requirements.txt
```

**Migration Issues**: Reset and recreate migrations if needed
```bash
python manage.py makemigrations tool_app
python manage.py migrate
```

**Static Files**: In development, Django serves static files automatically
```bash
# Check static files configuration
python manage.py findstatic filename.css
```

**File Processing**: Check file permissions and disk space
```bash
# Test file operations in Django shell
python manage.py shell
>>> from tool_app.views import compress_image
>>> # Test processing functions
```

### Development Workflow

1. Make model changes → `makemigrations` → `migrate`
2. Update views and forms together
3. Create/update templates with consistent styling
4. Test all conversion types thoroughly
5. Check error handling and user feedback

## Testing Strategy

- **Unit Tests**: Test individual processing functions
- **Integration Tests**: Test complete workflows
- **File Upload Tests**: Test with various file types and sizes
- **Error Handling**: Test invalid inputs and edge cases
- **API Tests**: Test JSON endpoints with curl or Postman

Example test command:
```bash
# Run all tests
python manage.py test

# Run with coverage
coverage run manage.py test
coverage report
```