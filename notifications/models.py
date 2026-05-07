# notifications/models.py

from django.db import models
from django.conf import settings
from listings.models import Listing, VisitRequest

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('visit_request', 'درخواست بازدید'),
        ('visit_approved', 'تایید بازدید'),
        ('visit_rejected', 'رد بازدید'),
        ('listing_approved', 'تایید آگهی'),
        ('listing_rejected', 'رد آگهی'),
        ('new_message', 'پیام جدید'),
    ]
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='گیرنده'
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        verbose_name='نوع اعلان'
    )
    title = models.CharField(max_length=200, verbose_name='عنوان')
    message = models.TextField(verbose_name='پیام')
    
    # لینک‌های مرتبط
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='آگهی'
    )
    visit_request = models.ForeignKey(
        VisitRequest,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='درخواست بازدید'
    )
    
    action_url = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='لینک عملیات'
    )
    
    is_read = models.BooleanField(default=False, verbose_name='خوانده شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'اعلان'
        verbose_name_plural = 'اعلان‌ها'
    
    def __str__(self):
        return f"{self.recipient.username} - {self.title}"
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save()
