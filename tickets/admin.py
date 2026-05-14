# tickets/admin.py

from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms

from .models import Ticket, TicketMessage, Category


class AdminReplyInlineForm(forms.ModelForm):
    class Meta:
        model = TicketMessage
        fields = ['message', 'attachment']


class AdminReplyInline(admin.StackedInline):
    model = TicketMessage
    form = AdminReplyInlineForm

    extra = 1
    max_num = 1

    fields = ('message', 'attachment')
    verbose_name = 'پاسخ پشتیبان'
    verbose_name_plural = 'ارسال پاسخ'

    def get_queryset(self, request):
        return super().get_queryset(request).none()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'subject',
        'user',
        'category',
        'priority',
        'status',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'status',
        'priority',
        'category',
        'created_at',
    )

    search_fields = (
        'subject',
        'user__username',
        'user__email',
    )

    readonly_fields = (
        'user',
        'subject',
        'category',
        'priority',
        'created_at',
        'updated_at',
        'display_messages',
    )

    inlines = [AdminReplyInline]

    fieldsets = (
        ('اطلاعات تیکت', {
            'fields': (
                'user',
                'subject',
                'category',
                'priority',
                'status',
            )
        }),

        ('گفتگو', {
            'fields': ('display_messages',)
        }),

        ('تاریخ‌ها', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )

    def display_messages(self, obj):
        if not obj.pk:
            return '-'

        messages = obj.messages.select_related('sender').all().order_by('created_at')

        html = """
        <div style="max-height:600px;overflow-y:auto;">
        """

        for msg in messages:

            sender_name = "پشتیبان" if msg.is_admin_reply else msg.sender.username

            bg_color = '#fff3cd' if msg.is_admin_reply else '#d1ecf1'
            border_color = '#ffc107' if msg.is_admin_reply else '#0dcaf0'

            html += f"""
            <div style="
                background:{bg_color};
                border-right:4px solid {border_color};
                padding:15px;
                margin-bottom:15px;
                border-radius:8px;
            ">
                <div style="display:flex;justify-content:space-between;margin-bottom:10px;">
                    <strong>{sender_name}</strong>
                    <small>{msg.created_at.strftime("%Y/%m/%d %H:%M")}</small>
                </div>

                <div style="line-height:1.8;white-space:pre-wrap;">
                    {msg.message}
                </div>
            """

            if msg.attachment:
                file_name = msg.attachment.name.split('/')[-1]

                html += f"""
                <div style="margin-top:10px;">
                    <a href="{msg.attachment.url}" target="_blank">
                        📎 {file_name}
                    </a>
                </div>
                """

            html += "</div>"

        html += "</div>"

        return mark_safe(html)

    display_messages.short_description = 'پیام‌های تیکت'

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:

            if isinstance(instance, TicketMessage):

                if not instance.message:
                    continue

                instance.ticket = form.instance
                instance.sender = request.user
                instance.is_admin_reply = True

                instance.save()

                # تغییر وضعیت تیکت
                form.instance.status = 'answered'
                form.instance.save()

        for obj in formset.deleted_objects:
            obj.delete()

        formset.save_m2m()


@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'ticket',
        'sender_display',
        'message_preview',
        'has_attachment',
        'created_at',
    )

    list_filter = (
        'is_admin_reply',
        'created_at',
    )

    search_fields = (
        'ticket__subject',
        'sender__username',
        'sender__email',
        'message',
    )

    readonly_fields = (
        'ticket',
        'sender',
        'message',
        'attachment',
        'is_admin_reply',
        'created_at',
    )

    def sender_display(self, obj):
        return "پشتیبان" if obj.is_admin_reply else obj.sender.username

    sender_display.short_description = 'فرستنده'

    def message_preview(self, obj):
        if len(obj.message) > 60:
            return obj.message[:60] + '...'
        return obj.message

    message_preview.short_description = 'متن پیام'

    def has_attachment(self, obj):
        return '✓' if obj.attachment else '✗'

    has_attachment.short_description = 'فایل'

    def has_add_permission(self, request):
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
    )

    search_fields = (
        'name',
    )
