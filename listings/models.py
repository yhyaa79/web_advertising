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
    
    name = models.CharField(max_length=100, verbose_name='نام')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, verbose_name='پلتفرم')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    
    class Meta:
        verbose_name = 'دسته‌بندی'
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



    ACTIVITY_CHOICES = [
        ('shopping_commerce', 'فروشگاهی و تجارت الکترونیک'),
        ('technology_software', 'تکنولوژی و نرم‌افزار '),
        ('education_learning', 'آموزش و یادگیری'),
        ('health_medicine_beauty', 'سلامت، پزشکی و زیبایی'),
        ('news_magazines_portals', 'خبری، مجله و پورتال'),
        ('finance_stock_exchange_cryptocurrency', 'مالی، بورس و ارز دیجیتال'),
        ('entertainment_games_movies', 'سرگرمی، بازی و فیلم'),
        ('lifestyle_fashion_fashion', 'سبک زندگی، مد و فشن'),
        ('travel_tourism_immigration', 'سفر، گردشگری و مهاجرت'),
        ('real_estate', 'املاک و مستغلات'),
        ('corporate_B2B_services', 'خدمات شرکتی و B2B'),
        ('sports_fitness', 'ورزشی و تناسب اندام'),
        ('food_cooking_restaurants', 'غذا، آشپزی و رستوران'),
        ('home_decoration_architecture', 'خانه، دکوراسیون و معماری'),
        ('pets', 'حیوانات خانگی'),
        ('other', 'سایر'),
    ]

    
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings', verbose_name='فروشنده')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='دسته‌بندی')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    location = models.CharField(max_length=200, null=True, blank=True, verbose_name='موقعیت')
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='قیمت')
    discount_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='قیمت با تخفیف')
    about_platform = models.TextField(null=True, blank=True, verbose_name='درباره پلتفرم')
    
    # اطلاعات پلتفرم
    platform_url = models.URLField(blank=True, verbose_name='آدرس پلتفرم')
    followers_count = models.IntegerField(default=0, blank=True, verbose_name='تعداد فالوور')
    monthly_income = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=0, verbose_name='درآمد ماهانه')
    platform_age = models.IntegerField(default=0, blank=True, verbose_name='سن پلتفرم (ماه)')
    
    most_like = models.IntegerField(null=True, blank=True, verbose_name='بیشترین لایک')
    most_view = models.IntegerField(null=True, blank=True, verbose_name='بیشترین بازدید')
    most_comment = models.IntegerField(null=True, blank=True, verbose_name='بیشترین کامنت')
    
    # تصویر اصلی
    main_image = models.ImageField(upload_to='listings/images/', verbose_name='تصویر اصلی')
    
    # ارتقا آگهی
    boost = models.BooleanField(default=False, verbose_name='آگهی پیشرفته')
    premier = models.BooleanField(default=False, verbose_name='آگهی برتر')
    
    # پیشنهاد قیمت 
    suggested_price = models.BooleanField(default=False, verbose_name='امکان پیشنهاد قیمت')

    # درآمد آگهی
    is_income = models.BooleanField(default=True, verbose_name='آگهی به درآمد رسیده')
    
    # اطلاعات مورد تایید
    is_verified = models.BooleanField(default=False, verbose_name='اطلاعات مورد تایید است')
    
    # گزینه خصوصی
    is_private = models.BooleanField(default=False, verbose_name='آگهی خصوصی')

    # حوزه‌های فعالیت 
    areas_activity = models.CharField(max_length=60, choices=ACTIVITY_CHOICES, verbose_name='حوزه‌ فعالیت')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    rejection_reason = models.TextField(blank=True, null=True, verbose_name='دلیل رد')
    views_count = models.IntegerField(default=0, verbose_name='تعداد بازدید')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    # فیلدهای درآمد و هزینه
    total_revenue = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='درآمد کل')
    total_profit = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='سود کل')
    avg_monthly_revenue = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='میانگین درآمد ماهانه')
    avg_monthly_profit = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='میانگین سود ماهانه')
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='حاشیه سود (درصد)')
    profit_multiplier = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='ضریب سود')
    revenue_multiplier = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='ضریب درآمد')
    
    # پشتیبانی پس از فروش
    post_sale_support = models.TextField(null=True, blank=True, verbose_name='پشتیبانی پس از فروش')
    
    class Meta:
        ordering = ['-boost', '-premier', '-created_at']
        verbose_name = 'آگهی'
        verbose_name_plural = 'آگهی‌ها'
    
    def __str__(self):
        return self.title
    

    def has_access(self, user):
        """
        Check if user can view full details of the listing
        """
        # اگر آگهی خصوصی نباشد همه دسترسی دارند
        if not self.is_private:
            return True

        # اگر کاربر لاگین نکرده باشد
        if not user.is_authenticated:
            return False

        # فروشنده همیشه دسترسی دارد
        if user == self.seller:
            return True

        # بررسی درخواست بازدید تایید شده
        return self.visit_requests.filter(requester=user, status='approved').exists()


    def get_income_chart_data(self):
        """Return income chart data as lists for labels and values"""
        income_points = self.income_data_points.all().order_by('date')
        labels = [point.date.strftime('%Y/%m/%d') for point in income_points]
        data = [float(point.income) for point in income_points]
        return {
            'labels': labels,
            'data': data
        }
    
    def get_views_chart_data(self):
        """Return views chart data as lists for labels and values"""
        views_points = self.views_data_points.all().order_by('date')
        labels = [point.date.strftime('%Y/%m/%d') for point in views_points]
        data = [point.views for point in views_points]
        return {
            'labels': labels,
            'data': data
        }
    
    def get_final_price(self):
        """Return the final price (discount price if available, otherwise regular price)"""
        return self.discount_price if self.discount_price else self.price
    
    def get_discount_percentage(self):
        """Calculate discount percentage"""
        if self.discount_price and self.price:
            return round(((self.price - self.discount_price) / self.price) * 100)
        return 0
    
    def calculate_roi(self):
        """Calculate Return on Investment"""
        if self.avg_monthly_profit and self.get_final_price():
            monthly_roi = (self.avg_monthly_profit / self.get_final_price()) * 100
            return round(monthly_roi, 2)
        return 0
    
    def get_payback_period(self):
        """Calculate payback period in months"""
        if self.avg_monthly_profit and self.avg_monthly_profit > 0:
            return round(self.get_final_price() / self.avg_monthly_profit, 1)
        return None


class ListingAnalyst(models.Model):
    """تحلیلگر و مشاور آگهی"""
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name='listing_analyst', verbose_name='آگهی')
    analyst_name = models.CharField(max_length=100, blank=True, verbose_name='نام تحلیلگر')
    analyst_expertise = models.CharField(max_length=200, blank=True, verbose_name='تخصص')
    analyst_education = models.CharField(max_length=200, blank=True, verbose_name='تحصیلات')
    analyst_record = models.CharField(max_length=200, blank=True, verbose_name='سابقه')
    analyst_image = models.ImageField(upload_to='analysts/', null=True, blank=True, verbose_name='تصویر تحلیلگر')
    analyst_description = models.TextField(blank=True, verbose_name='توضیحات تحلیلگر')
    
    class Meta:
        verbose_name = 'تحلیلگر'
        verbose_name_plural = 'تحلیلگران'
    
    def __str__(self):
        return f"تحلیلگر {self.listing.title}"


class SocialMedia(models.Model):
    """رسانه‌های اجتماعی"""
    PLATFORM_CHOICES = [
        ('twitter', 'توییتر'),
        ('instagram', 'اینستاگرام'),
        ('github', 'گیت‌هاب'),
        ('facebook', 'فیسبوک'),
        ('linkedin', 'لینکدین'),
        ('telegram', 'تلگرام'),
        ('other', 'سایر'),
    ]
    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='social_medias', verbose_name='آگهی')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, verbose_name='پلتفرم')
    followers = models.CharField(max_length=100, verbose_name='تعداد فالوور')
    url = models.URLField(blank=True, verbose_name='لینک')
    
    class Meta:
        verbose_name = 'رسانه اجتماعی'
        verbose_name_plural = 'رسانه‌های اجتماعی'
    
    def __str__(self):
        return f"{self.get_platform_display()} - {self.followers}"


class Attachment(models.Model):
    """پیوست‌ها"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='attachments', verbose_name='آگهی')
    file = models.FileField(upload_to='attachments/', verbose_name='فایل')
    
    class Meta:
        verbose_name = 'پیوست'
        verbose_name_plural = 'پیوست‌ها'
    
    def __str__(self):
        return self.file.name



class SaleInclude(models.Model):
    """فروش شامل - دارایی‌ها"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='sale_includes', verbose_name='آگهی')
    asset_name = models.CharField(max_length=200, verbose_name='نام دارایی')
    
    class Meta:
        verbose_name = 'دارایی فروش'
        verbose_name_plural = 'دارایی‌های فروش'
    
    def __str__(self):
        return self.asset_name


class License(models.Model):
    """مجوزها"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='licenses', verbose_name='آگهی')
    license_name = models.CharField(max_length=200, verbose_name='نام مجوز')
    
    class Meta:
        verbose_name = 'مجوز'
        verbose_name_plural = 'مجوزها'
    
    def __str__(self):
        return self.license_name
    

class ConfirmedInformation(models.Model):
    """اطلاعات تایید شده"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='confirmed', verbose_name='آگهی')
    confirmed_name = models.CharField(max_length=200, verbose_name='نام اطلاعات تایید شده')
    
    class Meta:
        verbose_name = 'اطلاعات تایید'
        verbose_name_plural = 'اطلاعاتات تایید'
    
    def __str__(self):
        return self.confirmed_name


class ServiceUsed(models.Model):
    """خدمات مورد استفاده"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='services_used', verbose_name='آگهی')
    service_name = models.CharField(max_length=200, verbose_name='نام خدمت')
    
    class Meta:
        verbose_name = 'خدمت مورد استفاده'
        verbose_name_plural = 'خدمات مورد استفاده'
    
    def __str__(self):
        return self.service_name


class MonetizationMethod(models.Model):
    """روش‌های کسب درآمد"""

    METHOD_CHOICES = [
        ('banner_click_advertising', 'تبلیغات بنری و کلیکی'),
        ('sponsored_posts', 'پست‌های حمایت‌شده'),
        ('cooperation_sales', 'همکاری در فروش'),
        ('special_subscription_sale', 'فروش اشتراک ویژه'),
        ('selling_digital_products', 'فروش محصولات دیجیتال'),
        ('selling_physical_products', 'فروش محصولات فیزیکی'),
        ('receive_financial_support', 'دریافت حمایت مالی'),
        ('holding_training_courses', 'برگزاری دوره‌های آموزشی و وبینار'),
        ('sell_​​backlinks', 'فروش بک‌لینک و فضای تبلیغاتی'),
        ('providing_consulting_services', 'ارائه خدمات مشاوره و فریلنسری'),
    ]

    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='monetization_methods', verbose_name='آگهی')
    method = models.CharField(max_length=50, choices=METHOD_CHOICES, verbose_name='روش')
    
    class Meta:
        verbose_name = 'روش کسب درآمد'
        verbose_name_plural = 'روش‌های کسب درآمد'
    
    def __str__(self):
        return self.method


class Expense(models.Model):
    """هزینه‌ها"""
    PERIOD_CHOICES = [
        ('monthly', 'ماهانه'),
        ('yearly', 'سالانه'),
        ('one_time', 'یکبار'),
    ]
    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='expenses', verbose_name='آگهی')
    expense_name = models.CharField(max_length=200, verbose_name='نام هزینه')
    amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='مبلغ')
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, verbose_name='دوره')
    
    class Meta:
        verbose_name = 'هزینه'
        verbose_name_plural = 'هزینه‌ها'
    
    def __str__(self):
        return f"{self.expense_name} - {self.amount}"


class IncomeDataPoint(models.Model):
    """نقاط داده برای نمودار درآمد"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='income_data_points', verbose_name='آگهی')
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
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='views_data_points', verbose_name='آگهی')
    date = models.DateField(verbose_name='تاریخ')
    views = models.IntegerField(verbose_name='بازدید')
    
    class Meta:
        verbose_name = 'نقطه داده بازدید'
        verbose_name_plural = 'نقاط داده بازدید'
        ordering = ['date']
        unique_together = ['listing', 'date']
    
    def __str__(self):
        return f"{self.listing.title} - {self.date}: {self.views}"


class ListingImage(models.Model):
    """تصاویر اضافی آگهی"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images', verbose_name='آگهی')
    image = models.ImageField(upload_to='listings/images/', verbose_name='تصویر')
    
    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'
    
    def __str__(self):
        return f"تصویر {self.listing.title}"


class VisitRequest(models.Model):
    """درخواست بازدید برای آگهی‌های خصوصی"""
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('approved', 'تایید شده'),
        ('rejected', 'رد شده'),
    ]
    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='visit_requests', verbose_name='آگهی')
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='درخواست‌کننده')
    message = models.TextField(blank=True, verbose_name='پیام')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درخواست')
    
    class Meta:
        verbose_name = 'درخواست بازدید'
        verbose_name_plural = 'درخواست‌های بازدید'
        unique_together = ['listing', 'requester']
    
    def __str__(self):
        return f"درخواست {self.requester.username} برای {self.listing.title}"


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



class ListingFAQ(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(blank=True, max_length=300, verbose_name='پرسش')
    answer = models.TextField(blank=True, verbose_name='پاسخ')
    order = models.PositiveIntegerField(blank=True, default=0, verbose_name='ترتیب')

    class Meta:
        verbose_name = 'پرسش و پاسخ'
        verbose_name_plural = 'پرسش‌ها و پاسخ‌ها'
        ordering = ['order', 'id']


    def __str__(self):
        return f"{self.listing.title} - {self.question}"
