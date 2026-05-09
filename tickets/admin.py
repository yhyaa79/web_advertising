# tickets/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Ticket, TicketMessage, Category

class AdminReplyInline(admin.StackedInline):
    model = TicketMessage
    extra = 1
    max_num = 1
    fields = ('message', 'attachment')
    verbose_name = 'پاسخ پشتیبان'
    verbose_name_plural = 'پاسخ جدید'
    
    def get_queryset(self, request):
        return super().get_queryset(request).none()

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'user', 'category', 'priority', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'priority', 'category', 'created_at')
    search_fields = ('subject', 'user__username', 'user__email')
    readonly_fields = ('user', 'subject', 'priority', 'category', 'created_at', 'updated_at', 'display_messages')
    inlines = [AdminReplyInline]
    
    fieldsets = (
        ('اطلاعات تیکت', {
            'fields': ('user', 'subject', 'category', 'priority', 'status')
        }),
        ('پیام‌ها', {
            'fields': ('display_messages',),
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def display_messages(self, obj):
        if not obj.pk:
            return '-'
        
        messages = obj.messages.all().order_by('created_at')
        html = '<div style="margin: 10px 0;">'
        
        for msg in messages:
            sender_label = "پشتیبان" if msg.is_admin_reply else msg.sender.username
            date_str = msg.created_at.strftime("%Y/%m/%d %H:%M")
            
            html += f'<div style="margin-bottom: 15px; padding: 10px; border: 1px solid #ddd;">'
            html += f'<div><strong>{sender_label}</strong> - {date_str}</div>'
            html += f'<div style="margin-top: 5px;">{msg.message}</div>'
            
            if msg.attachment:
                file_url = msg.attachment.url
                file_name = msg.attachment.name.split('/')[-1]
                html += f'<div style="margin-top: 5px;"><a href="{file_url}" target="_blank">📎 {file_name}</a></div>'
            
            html += '</div>'
        
        html += '</div>'
        return mark_safe(html)
    
    display_messages.short_description = 'پیام‌ها'
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, TicketMessage):
                if not instance.pk:
                    instance.sender = request.user
                    instance.is_admin_reply = True
                    instance.ticket = form.instance
                    instance.save()
                    form.instance.status = 'answered'
                    form.instance.save()
        
        for obj in formset.deleted_objects:
            obj.delete()

@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'sender_display', 'message_preview', 'has_attachment', 'created_at')
    list_filter = ('is_admin_reply', 'created_at')
    search_fields = ('ticket__subject', 'sender__username', 'message')
    readonly_fields = ('ticket', 'sender', 'is_admin_reply', 'created_at')
    
    def sender_display(self, obj):
        return "پشتیبان" if obj.is_admin_reply else obj.sender.username
    sender_display.short_description = 'فرستنده'
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'پیش‌نمایش'
    
    def has_attachment(self, obj):
        return "✓" if obj.attachment else "✗"
    has_attachment.short_description = 'فایل'
    
    def has_add_permission(self, request):
        return False

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
