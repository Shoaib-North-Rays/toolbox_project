from django.contrib import admin
from .models import FileConversion, Newsletter


@admin.register(FileConversion)
class FileConversionAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversion_type', 'status', 'created_at', 'original_filename')
    list_filter = ('conversion_type', 'status', 'created_at')
    search_fields = ('original_file', 'error_message')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ['-created_at']


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscribed_at', 'ip_address')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at', 'unsubscribed_at', 'ip_address', 'user_agent')
    ordering = ['-subscribed_at']
    
    actions = ['activate_subscriptions', 'deactivate_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        queryset.update(is_active=True, unsubscribed_at=None)
        self.message_user(request, f'{queryset.count()} subscriptions activated.')
    activate_subscriptions.short_description = 'Activate selected subscriptions'
    
    def deactivate_subscriptions(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_active=False, unsubscribed_at=timezone.now())
        self.message_user(request, f'{queryset.count()} subscriptions deactivated.')
    deactivate_subscriptions.short_description = 'Deactivate selected subscriptions'
