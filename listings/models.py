# listings/models.py

from django.db import models
from django.conf import settings

class Category(models.Model):
    PLATFORM_CHOICES = [
        ('website', 'وبسایت'),
        ('instagram', 'اینستاگرام'),
        ('telegram', 'تلگرام'),
        ('youtube', 'یوتیوب'),
        ('aparat', 'آپارات'),
        ('other', 'سایر'),
    ]
    
    name = models.CharField(max_length=100)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'دسته‌بندی‌ها'
    
    def __str__(self):
        return f"{self.name} ({self.get_platform_display()})"

class Listing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار تایید'),
        ('active', 'فعال'),
        ('sold', 'فروخته شده'),
        ('rejected', 'رد شده'),
        ('deleted', 'حذف شده'),
    ]
    
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True) # دسته بندی 
    title = models.CharField(max_length=200) # تیتر 
    description = models.TextField() #توضیحات 
    location = models.TextField(max_length=200, null=True, blank=True) # مکان 
    price = models.DecimalField(max_digits=12, decimal_places=0) # قیمت اصلی 
    discount_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True) # قیمت با تخفیف 
    
    # اطلاعات پلتفرم
    platform_url = models.URLField() # ادرس پلتفرم
    followers_count = models.IntegerField(default=0) # کاربر های پلتفرم
    monthly_income = models.DecimalField(max_digits=12, decimal_places=0) # درامد ماهانه
    platform_age = models.IntegerField(default=0) # سن پلتفرم

    most_like = models.IntegerField(null=True, blank=True) # بیشترین لایک 
    most_view = models.IntegerField(null=True, blank=True) # بیشترین بازدید 
    most_comment = models.IntegerField(null=True, blank=True) # بیشترین کامنت 
    
    # تصاویر و ویدیوها
    main_image = models.ImageField(upload_to='listings/images/') # تصویر اصلی 
    
    # ارتقا اگهی 
    is_preferment = models.BooleanField(default=False, verbose_name='آگهی ارتقا یافته')

    # گزینه خصوصی
    is_private = models.BooleanField(default=False, verbose_name='آگهی خصوصی') # گزینه خصوصی یا عمومی بودن اگهی 
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') # وضعیت اگهی 
    rejection_reason = models.TextField(blank=True, null=True, verbose_name='دلیل رد')
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def has_access(self, user):
        """بررسی دسترسی کاربر به جزئیات آگهی"""
        if not self.is_private:
            return True
        if user == self.seller:
            return True
        if user.is_authenticated:
            return VisitRequest.objects.filter(
                listing=self,
                requester=user,
                status='approved'
            ).exists()
        return False

class VisitRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار تایید'),
        ('approved', 'تایید شده'),
        ('rejected', 'رد شده'),
    ]
    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='visit_requests')
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='visit_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, verbose_name='پیام درخواست')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'درخواست بازدید'
        verbose_name_plural = 'درخواست‌های بازدید'
        unique_together = ['listing', 'requester']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"درخواست {self.requester.username} برای {self.listing.title}"

class IncomeProof(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='income_proofs')
    image = models.ImageField(upload_to='income_proofs/', verbose_name='تصویر اثبات درآمد', blank=True, null=True)
    description = models.TextField(blank=True, verbose_name='توضیحات')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'اثبات درآمد'
        verbose_name_plural = 'اثبات‌های درآمد'
    
    def __str__(self):
        return f"اثبات درآمد - {self.listing.title}"

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"تصویر {self.listing.title}"
