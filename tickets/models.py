# tickets/models.py


from django.db import models
from django.conf import settings
from django.utils import timezone


class TicketCategory(models.Model):
    """دسته‌بندی تیکت‌ها"""
    name = models.CharField(max_length=100, verbose_name='نام دسته')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    order = models.IntegerField(default=0, verbose_name='ترتیب نمایش')

    class Meta:
        verbose_name = 'دسته‌بندی تیکت'
        verbose_name_plural = 'دسته‌بندی‌های تیکت'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class TicketPriority(models.TextChoices):
    LOW = 'low', 'کم'
    MEDIUM = 'medium', 'متوسط'
    HIGH = 'high', 'زیاد'
    URGENT = 'urgent', 'فوری'


class TicketStatus(models.TextChoices):
    OPEN = 'open', 'باز'
    IN_PROGRESS = 'in_progress', 'در حال بررسی'
    WAITING_USER = 'waiting_user', 'در انتظار پاسخ کاربر'
    CLOSED = 'closed', 'بسته شده'


class Ticket(models.Model):
    """تیکت پشتیبانی"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets',
        verbose_name='کاربر'
    )
    category = models.ForeignKey(
        TicketCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tickets',
        verbose_name='دسته‌بندی'
    )
    subject = models.CharField(max_length=200, verbose_name='موضوع')
    priority = models.CharField(
        max_length=10,
        choices=TicketPriority.choices,
        default=TicketPriority.MEDIUM,
        verbose_name='اولویت'
    )
    status = models.CharField(
        max_length=20,
        choices=TicketStatus.choices,
        default=TicketStatus.OPEN,
        verbose_name='وضعیت'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')
    closed_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ بسته شدن')

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.user.username}"

    def close(self):
        """بستن تیکت"""
        self.status = TicketStatus.CLOSED
        self.closed_at = timezone.now()
        self.save()

    def reopen(self):
        """بازکردن مجدد تیکت"""
        self.status = TicketStatus.OPEN
        self.closed_at = None
        self.save()

    @property
    def is_closed(self):
        return self.status == TicketStatus.CLOSED

    @property
    def last_message(self):
        return self.messages.order_by('-created_at').first()


class TicketMessage(models.Model):
    """پیام‌های تیکت"""
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='تیکت'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ticket_messages',
        verbose_name='فرستنده'
    )
    message = models.TextField(verbose_name='پیام')
    attachment = models.FileField(
        upload_to='tickets/attachments/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='فایل پیوست'
    )
    is_staff_reply = models.BooleanField(default=False, verbose_name='پاسخ پشتیبانی')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال')

    class Meta:
        verbose_name = 'پیام تیکت'
        verbose_name_plural = 'پیام‌های تیکت'
        ordering = ['created_at']

    def __str__(self):
        return f"پیام {self.sender.username} در تیکت {self.ticket.id}"

    def save(self, *args, **kwargs):
        # تشخیص اینکه پیام از طرف پشتیبانی است یا کاربر
        if self.sender.is_staff:
            self.is_staff_reply = True
        super().save(*args, **kwargs)
