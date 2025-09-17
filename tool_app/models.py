from django.db import models
from django.utils import timezone
import os


def upload_to_files(instance, filename):
    """Generate upload path for files"""
    return f"uploads/{timezone.now().strftime('%Y/%m/%d')}/{filename}"


class FileConversion(models.Model):
    """Model to track file conversions"""
    CONVERSION_TYPES = [
        ('txt_to_pdf', 'Text to PDF'),
        ('pdf_to_txt', 'PDF to Text'),
        ('doc_to_pdf', 'DOC to PDF'),
        ('pdf_to_doc', 'PDF to DOC'),
        ('image_compress', 'Image Compression'),
        ('image_convert', 'Image Format Conversion'),
        ('qr_generate', 'QR Code Generation'),
        ('meta_tag_generator', 'Meta Tag Generator'),
        ('url_encoder', 'URL Encoder'),
        ('url_decoder', 'URL Decoder'),
        ('domain_ip_resolver', 'Domain to IP Resolver'),
        ('whois_lookup', 'Whois Lookup'),
        ('robots_sitemap_generator', 'Robots.txt & Sitemap Generator'),
        ('hash_generator', 'Hash Generator'),
        ('jwt_decoder', 'JWT Decoder'),
        ('ssl_checker', 'SSL Certificate Checker'),
        ('email_validator', 'Email Validator'),
        ('text_encryption', 'Text Encryption/Decryption'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    original_file = models.FileField(upload_to=upload_to_files)
    converted_file = models.FileField(upload_to=upload_to_files, blank=True, null=True)
    conversion_type = models.CharField(max_length=30, choices=CONVERSION_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    error_message = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_conversion_type_display()} - {self.status}"
    
    @property
    def original_filename(self):
        return os.path.basename(self.original_file.name) if self.original_file else None
    
    @property
    def converted_filename(self):
        return os.path.basename(self.converted_file.name) if self.converted_file else None
