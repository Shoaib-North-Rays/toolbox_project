from django.urls import path
from . import views

app_name = 'tool_app'

urlpatterns = [
    # Web views
    path('', views.home, name='home'),
    path('file-converter/', views.file_converter, name='file_converter'),
    path('text-to-pdf/', views.text_to_pdf, name='text_to_pdf'),
    path('result/<int:pk>/', views.conversion_result, name='conversion_result'),
    path('download/<int:pk>/', views.download_file, name='download_file'),
    
    # API endpoints
    path('api/convert/', views.api_convert_file, name='api_convert_file'),
    path('api/text-to-pdf/', views.api_text_to_pdf, name='api_text_to_pdf'),
    path('api/status/<int:pk>/', views.api_conversion_status, name='api_conversion_status'),
]