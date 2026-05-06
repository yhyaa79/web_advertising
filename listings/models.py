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
    
    """LEVEL_CHOICES = [
        ('beginner', 'مبتدی'),
        ('intermediate', 'متوسط'),
        ('advanced', 'پیشرفته'),
        ('professional', 'حرفه‌ای'),
    ] """
    
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.TextField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    discount_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    
    # سطح آگهی
    """ level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner', verbose_name='سطح') """
    
    # اطلاعات پلتفرم
    platform_url = models.URLField()
    followers_count = models.IntegerField(default=0)
    monthly_income = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=0)
    platform_age = models.IntegerField(default=0)

    most_like = models.IntegerField(null=True, blank=True)
    most_view = models.IntegerField(null=True, blank=True)
    most_comment = models.IntegerField(null=True, blank=True)
    
    # تصاویر و ویدیوها
    main_image = models.ImageField(upload_to='listings/images/')
    
    # ارتقا اگهی 
    is_preferment = models.BooleanField(default=False, verbose_name='آگهی ارتقا یافته')

    # درامد اگهی 
    is_income = models.BooleanField(default=True, verbose_name='اگهی به درامد رسیده')

    # اطلاعات مورد تایید 
    is_verified = models.BooleanField(default=False, verbose_name='اطلاعات مورد تایید است')

    # گزینه خصوصی
    is_private = models.BooleanField(default=False, verbose_name='آگهی خصوصی')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True, null=True, verbose_name='دلیل رد')
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_final_price(self):
        """قیمت نهایی (با تخفیف یا بدون تخفیف)"""
        return self.discount_price if self.discount_price else self.price
    
    def get_roi_months(self):
        """محاسبه تعداد ماه‌های برگشت سرمایه"""
        if self.monthly_income and self.monthly_income > 0:
            final_price = self.get_final_price()
            return final_price / self.monthly_income
        return None
    
    def get_roi_display(self):
        """نمایش برگشت سرمایه به صورت ماه"""
        roi_months = self.get_roi_months()
        if roi_months is None:
            return "نامشخص"
        
        months = int(roi_months)
        return f"{months} ماه"
    
    def get_income_chart_data(self):
        """دریافت داده‌های نمودار درآمد"""
        data_points = self.income_data_points.all().order_by('date')
        if not data_points.exists():
            return None
        return {
            'labels': [point.date.strftime('%Y/%m/%d') for point in data_points],
            'data': [float(point.income) for point in data_points]
        }
    
    def get_views_chart_data(self):
        """دریافت داده‌های نمودار بازدید"""
        data_points = self.views_data_points.all().order_by('date')
        if not data_points.exists():
            return None
        return {
            'labels': [point.date.strftime('%Y/%m/%d') for point in data_points],
            'data': [point.views for point in data_points]
        }
    
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


class IncomeDataPoint(models.Model):
    """نقاط داده برای نمودار درآمد"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='income_data_points')
    date = models.DateField(verbose_name='تاریخ')
    income = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='درآمد')
    
    class Meta:
        verbose_name = 'نقطه داده درآمد'
        verbose_name_plural = 'نقاط داده درآمد'
        ordering = ['date']
        unique_together = ['listing', 'date']
    
    def __str__(self):
        return f"{self.listing.title} - {self.date}: {self.income}"


class ViewsDataPoint(models.Model):
    """نقاط داده برای نمودار بازدید"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='views_data_points')
    date = models.DateField(verbose_name='تاریخ')
    views = models.IntegerField(verbose_name='بازدید')
    
    class Meta:
        verbose_name = 'نقطه داده بازدید'
        verbose_name_plural = 'نقاط داده بازدید'
        ordering = ['date']
        unique_together = ['listing', 'date']
    
    def __str__(self):
        return f"{self.listing.title} - {self.date}: {self.views}"


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
