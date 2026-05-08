# payments/admin.py

from django.contrib import admin
from .models import Transaction, PriceProposal, Dispute, ChatRoom, ChatMessage


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['tracking_code', 'buyer', 'seller', 'listing', 'amount', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'payment_date']
    search_fields = ['tracking_code', 'buyer__username', 'seller__username', 'listing__title']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('buyer', 'seller', 'listing', 'tracking_code')
        }),
        ('اطلاعات مالی', {
            'fields': ('amount', 'commission', 'status')
        }),
        ('تاریخ‌ها', {
            'fields': ('payment_date', 'completion_date', 'created_at', 'updated_at')
        }),
    )


@admin.register(PriceProposal)
class PriceProposalAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'seller', 'listing', 'proposed_price', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'buyer_agreed', 'seller_agreed']
    search_fields = ['buyer__username', 'seller__username', 'listing__title']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('اطلاعات پیشنهاد', {
            'fields': ('listing', 'buyer', 'seller', 'proposed_price', 'message')
        }),
        ('وضعیت', {
            'fields': ('status', 'seller_response')
        }),
        ('توافق', {
            'fields': ('buyer_agreed', 'seller_agreed', 'buyer_cancelled', 'seller_cancelled')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    list_display = ['id', 'transaction', 'opened_by', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'resolved_at']
    search_fields = ['transaction__tracking_code', 'opened_by__username', 'reason']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('اطلاعات اختلاف', {
            'fields': ('transaction', 'opened_by', 'reason', 'status')
        }),
        ('بررسی ادمین', {
            'fields': ('admin_notes', 'resolution', 'resolved_at')
        }),
        ('تاریخ', {
            'fields': ('created_at',)
        }),
    )


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ['sender', 'message', 'is_read', 'created_at']
    can_delete = False


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'seller', 'listing', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['buyer__username', 'seller__username', 'listing__title']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ChatMessageInline]
    date_hierarchy = 'created_at'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_room', 'sender', 'message_preview', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__username', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'پیام'
