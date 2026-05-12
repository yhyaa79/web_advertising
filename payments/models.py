# payments/models.py

from django.db import models
from django.conf import settings
from listings.models import Listing

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('in_escrow', 'در حساب امن'),
        ('completed', 'تکمیل شده'),
        ('cancelled', 'لغو شده'),
        ('refunded', 'بازگشت داده شده'),
    ]
    
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sales')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    commission = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    payment_date = models.DateTimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    
    tracking_code = models.CharField(max_length=50, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"تراکنش {self.tracking_code}"


class PriceProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار پاسخ'),
        ('accepted', 'پذیرفته شده'),
        ('rejected', 'رد شده'),
        ('cancelled', 'لغو شده'),
        ('negotiating', 'در حال گفتگو'),
        ('deal_confirmed', 'توافق شد'),
        ('deal_cancelled', 'کنسل شد'),
        
    ]
    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='price_proposals')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_proposals')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_proposals')
    
    proposed_price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='قیمت پیشنهادی')
    message = models.TextField(blank=True, verbose_name='پیام')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    seller_response = models.TextField(blank=True, verbose_name='پاسخ فروشنده')
    
    # فیلدهای جدید برای توافق
    buyer_agreed = models.BooleanField(default=False, verbose_name='خریدار موافق')
    seller_agreed = models.BooleanField(default=False, verbose_name='فروشنده موافق')
    buyer_cancelled = models.BooleanField(default=False, verbose_name='خریدار کنسل کرد')
    seller_cancelled = models.BooleanField(default=False, verbose_name='فروشنده کنسل کرد')
    buyer_rejected = models.BooleanField(default=False)  # جدید
    seller_rejected = models.BooleanField(default=False)  # جدید
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        verbose_name = 'پیشنهاد قیمت'
        verbose_name_plural = 'پیشنهادهای قیمت'
        ordering = ['-created_at']
        unique_together = ['listing', 'buyer']
    
    def __str__(self):
        return f"پیشنهاد {self.buyer.username} برای {self.listing.title}"


class Dispute(models.Model):
    STATUS_CHOICES = [
        ('open', 'باز'),
        ('in_review', 'در حال بررسی'),
        ('resolved', 'حل شده'),
        ('closed', 'بسته شده'),
    ]
    
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='disputes')
    opened_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    
    admin_notes = models.TextField(blank=True)
    resolution = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"اختلاف {self.transaction.tracking_code}"


class ChatRoom(models.Model):
    """اتاق چت بین خریدار و فروشنده برای یک آگهی"""
    proposal = models.OneToOneField(PriceProposal, on_delete=models.CASCADE, related_name='chat_room')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='buyer_chats')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_chats')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='chat_rooms')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'اتاق چت'
        verbose_name_plural = 'اتاق‌های چت'
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"چت {self.buyer.username} و {self.seller.username} - {self.listing.title}"


class ChatMessage(models.Model):
    """پیام‌های چت"""
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(verbose_name='پیام')
    
    is_read = models.BooleanField(default=False, verbose_name='خوانده شده')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'پیام چت'
        verbose_name_plural = 'پیام‌های چت'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender.username}: {self.message[:30]}"
