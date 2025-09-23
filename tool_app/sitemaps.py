from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from datetime import datetime


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.8
    changefreq = 'weekly'
    
    def items(self):
        return [
            'tool_app:home',
            'tool_app:about', 
            'tool_app:contact',
            'tool_app:blog',
            'tool_app:privacy_policy',
            'tool_app:terms',
            'tool_app:disclaimer'
        ]
    
    def location(self, item):
        return reverse(item)
    
    def lastmod(self, obj):
        return datetime.now()


class ToolViewSitemap(Sitemap):
    """Sitemap for tool pages"""
    priority = 0.9
    changefreq = 'monthly'
    
    def items(self):
        return [
            # File Tools
            'tool_app:file_converter',
            'tool_app:text_to_pdf',
            
            # Image Tools
            'tool_app:image_compression',
            'tool_app:image_conversion',
            
            # Web & SEO Tools
            'tool_app:qr_code_generator',
            'tool_app:meta_tag_generator',
            'tool_app:url_encoder_decoder',
            'tool_app:domain_ip_resolver',
            'tool_app:whois_lookup',
            'tool_app:robots_sitemap_generator',
            
            # Security & Utility Tools
            'tool_app:hash_generator',
            'tool_app:jwt_decoder',
            'tool_app:ssl_checker',
            'tool_app:email_validator',
            'tool_app:text_encryption',
            
            # Fun & Engagement Tools
            'tool_app:meme_generator',
            'tool_app:emoji_translator',
            'tool_app:random_quote',
            'tool_app:random_name',
            'tool_app:unit_converter',
            
            # Audio/Video Tools
            'tool_app:audio_converter',
            'tool_app:audio_speed_changer',
            'tool_app:video_to_audio',
        ]
    
    def location(self, item):
        return reverse(item)
    
    def lastmod(self, obj):
        return datetime.now()


# Sitemap dictionary
sitemaps = {
    'static': StaticViewSitemap,
    'tools': ToolViewSitemap,
}