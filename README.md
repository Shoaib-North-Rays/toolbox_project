# Toolbox Project

A production-ready Django web application providing online file conversion tools built with Django MVT architecture and Tailwind CSS.

## Features

- **File Converter**: Convert between TXT, PDF, DOC, and DOCX formats
- **Text to PDF**: Convert plain text to formatted PDF documents
- **Responsive Design**: Mobile-friendly interface using Tailwind CSS
- **JSON API**: RESTful API endpoints for programmatic access
- **Secure Processing**: Files are processed securely with validation
- **Production Ready**: Proper settings, error handling, and file management

## Tech Stack

- **Backend**: Django 4.2.7
- **Frontend**: Tailwind CSS (via CDN)
- **Database**: SQLite (development) / PostgreSQL (production)
- **File Processing**: ReportLab (PDF generation), python-docx (Word documents)
- **Styling**: Tailwind CSS with responsive design

## Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd toolbox_project
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Visit the application**:
   Open your browser and go to `http://127.0.0.1:8000/`

## Project Structure

```
toolbox_project/
├── toolbox_project/        # Django project settings
│   ├── __init__.py
│   ├── settings.py         # Project settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── tool_app/               # Main application
│   ├── migrations/         # Database migrations
│   ├── templates/          # HTML templates
│   │   └── tool_app/       # App-specific templates
│   ├── __init__.py
│   ├── admin.py           # Admin interface
│   ├── apps.py            # App configuration
│   ├── forms.py           # Django forms
│   ├── models.py          # Database models
│   ├── urls.py            # App URL routing
│   └── views.py           # View functions
├── templates/              # Global templates
│   └── base.html          # Base template
├── static/                 # Static files (CSS, JS, images)
├── media/                  # Uploaded files
├── requirements.txt        # Python dependencies
├── manage.py              # Django management script
└── README.md              # This file
```

## Available Tools

### 1. File Converter
- **URL**: `/file-converter/`
- **Supported conversions**:
  - TXT → PDF
  - PDF → TXT (demo)
  - DOC/DOCX → PDF
  - PDF → DOC (demo)

### 2. Text to PDF
- **URL**: `/text-to-pdf/`
- Convert plain text to formatted PDF documents
- Optional document title
- Professional formatting with proper margins and typography

## API Endpoints

The application provides RESTful API endpoints:

### File Conversion API
- **Endpoint**: `POST /api/convert/`
- **Parameters**:
  - `file`: File to convert
  - `conversion_type`: Type of conversion (e.g., 'txt_to_pdf')
- **Response**: JSON with conversion details and download URL

### Text to PDF API
- **Endpoint**: `POST /api/text-to-pdf/`
- **Parameters** (JSON):
  ```json
  {
    "text_content": "Your text here",
    "title": "Document Title (optional)"
  }
  ```
- **Response**: JSON with base64-encoded PDF data

### Conversion Status API
- **Endpoint**: `GET /api/status/<conversion_id>/`
- **Response**: JSON with conversion status and details

### Example API Usage

```python
import requests

# File conversion
with open('document.txt', 'rb') as f:
    response = requests.post('http://localhost:8000/api/convert/', {
        'conversion_type': 'txt_to_pdf'
    }, files={'file': f})

# Text to PDF
response = requests.post('http://localhost:8000/api/text-to-pdf/', json={
    'text_content': 'Hello, World!',
    'title': 'My Document'
})
```

## Development

### Adding New Tools

1. **Add conversion logic** in `tool_app/views.py`
2. **Create forms** in `tool_app/forms.py` if needed
3. **Add URL patterns** in `tool_app/urls.py`
4. **Create templates** in `tool_app/templates/tool_app/`
5. **Update navigation** in `templates/base.html`

### Database Models

The `FileConversion` model tracks all file conversions:
- Original and converted file paths
- Conversion type and status
- Error messages and timestamps
- Created/updated timestamps

### File Storage

- **Uploaded files**: Stored in `media/uploads/YYYY/MM/DD/`
- **File size limit**: 10MB (configurable in forms)
- **Supported formats**: TXT, PDF, DOC, DOCX

## Deployment

### Production Settings

1. **Update settings for production**:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use PostgreSQL database
   - Set up proper static file serving

2. **Environment Variables**:
   ```bash
   export SECRET_KEY="your-secret-key"
   export DEBUG="False"
   export DATABASE_URL="postgresql://..."
   ```

3. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

### Docker Deployment (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
- Create an issue on the repository
- Check the Django documentation
- Review the code comments for implementation details

## Future Enhancements

- [ ] Add more file format support (Excel, PowerPoint, Images)
- [ ] Implement batch file conversion
- [ ] Add user accounts and conversion history
- [ ] OCR support for scanned documents
- [ ] Real-time conversion progress tracking
- [ ] Advanced PDF manipulation tools