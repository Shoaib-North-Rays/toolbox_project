from django.urls import path
from . import views

app_name = 'tool_app'

urlpatterns = [
    # Web views
    path('', views.home, name='home'),
    path('file-converter/', views.file_converter, name='file_converter'),
    path('text-to-pdf/', views.text_to_pdf, name='text_to_pdf'),
    path('image-compression/', views.image_compression, name='image_compression'),
    path('image-conversion/', views.image_conversion, name='image_conversion'),
    path('qr-code-generator/', views.qr_code_generator, name='qr_code_generator'),
    path('meta-tag-generator/', views.meta_tag_generator, name='meta_tag_generator'),
    path('url-encoder-decoder/', views.url_encoder_decoder, name='url_encoder_decoder'),
    path('domain-ip-resolver/', views.domain_ip_resolver, name='domain_ip_resolver'),
    path('whois-lookup/', views.whois_lookup, name='whois_lookup'),
    path('robots-sitemap-generator/', views.robots_sitemap_generator, name='robots_sitemap_generator'),
    
    # Security & Utility Tools
    path('hash-generator/', views.hash_generator, name='hash_generator'),
    path('jwt-decoder/', views.jwt_decoder, name='jwt_decoder'),
    path('ssl-checker/', views.ssl_checker, name='ssl_checker'),
    path('email-validator/', views.email_validator, name='email_validator'),
    path('text-encryption/', views.text_encryption, name='text_encryption'),
    
    # Fun & Engagement Tools
    path('meme-generator/', views.meme_generator, name='meme_generator'),
    path('emoji-translator/', views.emoji_translator, name='emoji_translator'),
    path('random-quote/', views.random_quote, name='random_quote'),
    path('random-name/', views.random_name, name='random_name'),
    path('unit-converter/', views.unit_converter, name='unit_converter'),
    
    # Audio/Video Tools
    path('audio-converter/', views.audio_converter, name='audio_converter'),
    path('audio-speed-changer/', views.audio_speed_changer, name='audio_speed_changer'),
    path('video-to-audio/', views.video_to_audio, name='video_to_audio'),
    
    path('result/<int:pk>/', views.conversion_result, name='conversion_result'),
    path('download/<int:pk>/', views.download_file, name='download_file'),
    
    # Static Pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms/', views.terms, name='terms'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),
    path('blog/', views.blog, name='blog'),
    path('task_manager/', views.task_manager, name='task_manager'),
    path('voice_clone/', views.voice_clone, name='voice_clone')
    
    # API endpoints
    path('api/convert/', views.api_convert_file, name='api_convert_file'),
    path('api/text-to-pdf/', views.api_text_to_pdf, name='api_text_to_pdf'),
    path('api/status/<int:pk>/', views.api_conversion_status, name='api_conversion_status'),
    path('api/newsletter-subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]
