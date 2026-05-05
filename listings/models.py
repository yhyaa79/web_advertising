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
    ]
    
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=0)
    
    # اطلاعات پلتفرم
    platform_url = models.URLField()
    followers_count = models.IntegerField(default=0)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=0)
    
    # تصاویر و ویدیوها
    main_image = models.ImageField(upload_to='listings/images/')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class IncomeProof(models.Model):
    PROOF_TYPE_CHOICES = [
        ('screenshot', 'اسکرین‌شات'),
        ('video', 'ویدیو'),
    ]
    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='income_proofs')
    proof_type = models.CharField(max_length=20, choices=PROOF_TYPE_CHOICES)
    file = models.FileField(upload_to='income_proofs/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"اثبات درآمد - {self.listing.title}"

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"تصویر {self.listing.title}"
