# tickets/models.py

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import os

def validate_file_size(file):
    max_size = 10 * 1024 * 1024  # 10MB
    if file.size > max_size:
        raise ValidationError('حجم فایل نباید بیشتر از 10 مگابایت باشد.')

def ticket_attachment_path(instance, filename):
    return f'tickets/{instance.ticket.id}/{filename}'

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام دسته‌بندی')
    
    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'
    
    def __str__(self):
        return self.name


# tickets/models.py

class Ticket(models.Model):

    STATUS_CHOICES = [
        ('open', 'باز'),
        ('answered', 'پاسخ داده شده'),
        ('closed', 'بسته شده'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'کم'),
        ('medium', 'متوسط'),
        ('high', 'بالا'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets',
        verbose_name='کاربر'
    )

    subject = models.CharField(max_length=200, verbose_name='موضوع')

    # این قسمت اصلاح شد
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='tickets',
        verbose_name='دسته‌بندی'
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name='اولویت'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='open',
        verbose_name='وضعیت'
    )

    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets', verbose_name='کاربر')
    subject = models.CharField(max_length=200, verbose_name='موضوع')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets', verbose_name='دسته‌بندی')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name='اولویت')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open', verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت‌ها'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"#{self.id} - {self.subject}"
    
    def has_admin_reply(self):
        last_message = self.messages.last()
        if last_message and last_message.is_admin_reply:
            return True
        return False
    
    def get_last_message(self):
        return self.messages.last()


class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages', verbose_name='تیکت')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='فرستنده')
    message = models.TextField(verbose_name='پیام')
    attachment = models.FileField(upload_to=ticket_attachment_path, blank=True, null=True, validators=[validate_file_size], verbose_name='فایل پیوست')
    is_admin_reply = models.BooleanField(default=False, verbose_name='پاسخ ادمین')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال')
    
    class Meta:
        verbose_name = 'پیام تیکت'
        verbose_name_plural = 'پیام‌های تیکت'
        ordering = ['created_at']
    
    def __str__(self):
        sender_type = "پشتیبان" if self.is_admin_reply else "کاربر"
        return f"{sender_type} - تیکت #{self.ticket.id}"
    
    def get_file_extension(self):
        if self.attachment:
            return os.path.splitext(self.attachment.name)[1].lower()
        return None
