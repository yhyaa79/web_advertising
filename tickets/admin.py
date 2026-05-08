# tickets/admin.py


from django.contrib import admin
from .models import TicketCategory, Ticket, TicketMessage


@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    search_fields = ['name']


class TicketMessageInline(admin.TabularInline):
    model = TicketMessage
    extra = 0
    readonly_fields = ['sender', 'created_at', 'is_staff_reply']
    fields = ['sender', 'message', 'attachment', 'is_staff_reply', 'created_at']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'user', 'category', 'priority', 'status', 'created_at']
    list_filter = ['status', 'priority', 'category', 'created_at']
    search_fields = ['subject', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'closed_at']
    inlines = [TicketMessageInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('user', 'category', 'subject')
        }),
        ('وضعیت', {
            'fields': ('status', 'priority')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at', 'closed_at')
        }),
    )


@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'ticket', 'sender', 'is_staff_reply', 'created_at']
    list_filter = ['is_staff_reply', 'created_at']
    search_fields = ['message', 'ticket__subject', 'sender__username']
    readonly_fields = ['created_at', 'is_staff_reply']
