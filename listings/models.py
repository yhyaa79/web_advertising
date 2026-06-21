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

    # ─── وضعیت ───────────────────────────────────────────────
    STATUS_CHOICES = [
        ('pending',  'در انتظار تایید'),
        ('active',   'فعال'),
        ('sold',     'فروخته شده'),
        ('rejected', 'رد شده'),
        ('deleted',  'حذف شده'),
    ]

    # ─── حوزه فعالیت ─────────────────────────────────────────
    ACTIVITY_CHOICES = [
        ('shopping_commerce',                'فروشگاهی و تجارت الکترونیک'),
        ('technology_software',              'تکنولوژی و نرم‌افزار'),
        ('education_learning',               'آموزش و یادگیری'),
        ('health_medicine_beauty',           'سلامت، پزشکی و زیبایی'),
        ('news_magazines_portals',           'خبری، مجله و پورتال'),
        ('finance_stock_exchange_cryptocurrency', 'مالی، بورس و ارز دیجیتال'),
        ('entertainment_games_movies',       'سرگرمی، بازی و فیلم'),
        ('lifestyle_fashion_fashion',        'سبک زندگی، مد و فشن'),
        ('travel_tourism_immigration',       'سفر، گردشگری و مهاجرت'),
        ('real_estate',                      'املاک و مستغلات'),
        ('corporate_B2B_services',           'خدمات شرکتی و B2B'),
        ('sports_fitness',                   'ورزشی و تناسب اندام'),
        ('food_cooking_restaurants',         'غذا، آشپزی و رستوران'),
        ('home_decoration_architecture',     'خانه، دکوراسیون و معماری'),
        ('pets',                             'حیوانات خانگی'),
        ('other',                            'سایر'),
    ]

    # ─── دلیل واگذاری ────────────────────────────────────────
    SALE_REASON_CHOICES = [
        ('focus_other_projects', 'تمرکز روی پروژه‌های دیگر'),
        ('lack_of_time',         'نداشتن زمان کافی'),
        ('need_capital',         'نیاز به سرمایه و پول نقد'),
        ('immigration',          'مهاجرت'),
        ('career_change',        'تغییر شغل یا بازنشستگی'),
        ('partner_dispute',      'اختلاف با شرکا / انحلال تیم'),
        ('growth_ceiling',       'رسیدن به سقف رشد فردی'),
        ('personal_health',      'دلایل شخصی / سلامتی'),
    ]

    # ─── نوع فروش ────────────────────────────────────────────
    SALE_TYPE_CHOICES = [
        ('full_ownership',    'فروش مالکیت / انتقال کامل'),
        ('partial_ownership', 'فروش مالکیت بخشی / سهمی'),
        ('license',           'فروش مجوز / لایسنس'),
        ('revenue_share',     'فروش سهم از درآمد'),
        ('brand',             'فروش برند'),
    ]

    # ─── فیلدهای مشترک ───────────────────────────────────────
    seller   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='listings', verbose_name='فروشنده')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, blank=True, verbose_name='دسته‌بندی')
    title       = models.CharField(max_length=200, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    location    = models.CharField(max_length=200, null=True, blank=True, verbose_name='موقعیت')
    price          = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='قیمت')
    discount_price = models.DecimalField(max_digits=12, decimal_places=0,
                                         null=True, blank=True, verbose_name='قیمت با تخفیف')
    about_platform = models.TextField(null=True, blank=True, verbose_name='درباره پلتفرم')

    platform_url    = models.URLField(blank=True, verbose_name='آدرس پلتفرم')
    followers_count = models.IntegerField(default=0, blank=True, verbose_name='تعداد فالوور')
    monthly_income  = models.DecimalField(null=True, blank=True, max_digits=12,
                                          decimal_places=0, verbose_name='درآمد ماهانه')
    platform_age    = models.IntegerField(default=0, blank=True, verbose_name='سن پلتفرم (ماه)')

    most_like    = models.IntegerField(null=True, blank=True, verbose_name='بیشترین لایک')
    most_view    = models.IntegerField(null=True, blank=True, verbose_name='بیشترین بازدید')
    most_comment = models.IntegerField(null=True, blank=True, verbose_name='بیشترین کامنت')

    main_image = models.ImageField(upload_to='listings/images/', verbose_name='تصویر اصلی')

    boost          = models.BooleanField(default=False, verbose_name='آگهی پیشرفته')
    premier        = models.BooleanField(default=False, verbose_name='آگهی برتر')
    suggested_price = models.BooleanField(default=False, verbose_name='امکان پیشنهاد قیمت')
    is_income      = models.BooleanField(default=True,  verbose_name='آگهی به درآمد رسیده')
    is_verified    = models.BooleanField(default=False, verbose_name='اطلاعات مورد تایید است')
    is_private     = models.BooleanField(default=False, verbose_name='آگهی خصوصی')

    areas_activity = models.CharField(max_length=60, choices=ACTIVITY_CHOICES,
                                      verbose_name='حوزه‌ فعالیت')

    status           = models.CharField(max_length=20, choices=STATUS_CHOICES,
                                        default='pending', verbose_name='وضعیت')
    rejection_reason = models.TextField(blank=True, null=True, verbose_name='دلیل رد')
    views_count      = models.IntegerField(default=0, verbose_name='تعداد بازدید')
    created_at       = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at       = models.DateTimeField(auto_now=True,     verbose_name='تاریخ بروزرسانی')

    total_revenue        = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='درآمد کل')
    total_profit         = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='سود کل')
    avg_monthly_revenue  = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='میانگین درآمد ماهانه')
    avg_monthly_profit   = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='میانگین سود ماهانه')
    profit_margin        = models.DecimalField(max_digits=5,  decimal_places=2, null=True, blank=True, verbose_name='حاشیه سود (درصد)')
    profit_multiplier    = models.DecimalField(max_digits=5,  decimal_places=2, null=True, blank=True, verbose_name='ضریب سود')
    revenue_multiplier   = models.DecimalField(max_digits=5,  decimal_places=2, null=True, blank=True, verbose_name='ضریب درآمد')

    post_sale_support = models.TextField(null=True, blank=True, verbose_name='پشتیبانی پس از فروش')

    # دلیل واگذاری
    sale_reason             = models.CharField(max_length=30, choices=SALE_REASON_CHOICES,
                                               null=True, blank=True, verbose_name='دلیل واگذاری')
    sale_reason_description = models.TextField(null=True, blank=True,
                                               verbose_name='توضیحات دلیل واگذاری')

    # ════════════════════════════════════════════════════════
    # نوع فروش
    # ════════════════════════════════════════════════════════
    sale_type = models.CharField(
        max_length=20, choices=SALE_TYPE_CHOICES,
        null=True, blank=True, verbose_name='نوع فروش'
    )

    # ── 1. فروش مالکیت / انتقال کامل ────────────────────────
    ownership_document_status = models.CharField(
        max_length=200, null=True, blank=True,
        verbose_name='وضعیت مالکیت / اسناد'
    )
    ownership_transfer_conditions = models.TextField(
        null=True, blank=True,
        verbose_name='شرایط انتقال مالکیت'
    )

    # ── 2. فروش مالکیت بخشی / سهمی ──────────────────────────
    partial_ownership_percentage = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        verbose_name='درصد سهم'
    )
    partial_ownership_valuation_method = models.TextField(
        null=True, blank=True,
        verbose_name='فرمول / روش ارزش‌گذاری'
    )
    partial_ownership_buyer_rights = models.TextField(
        null=True, blank=True,
        verbose_name='حقوق خریدار'
    )
    partial_ownership_exit_conditions = models.TextField(
        null=True, blank=True,
        verbose_name='شرایط خروج / فروش مجدد سهم'
    )

    # ── 3. فروش مجوز / لایسنس ────────────────────────────────
    LICENSE_DURATION_CHOICES = [
        ('permanent', 'دائمی'),
        ('limited',   'مدت‌دار'),
    ]
    license_duration_type = models.CharField(
        max_length=20, choices=LICENSE_DURATION_CHOICES,
        null=True, blank=True,
        verbose_name='نوع مدت مجوز'
    )
    license_duration_months = models.IntegerField(
        null=True, blank=True,
        verbose_name='مدت مجوز (ماه)'
    )
    license_scope = models.TextField(
        null=True, blank=True,
        verbose_name='محدوده مجوز'
    )
    license_restrictions = models.TextField(
        null=True, blank=True,
        verbose_name='محدودیت‌های مجوز'
    )

    # ── 4. فروش سهم از درآمد ─────────────────────────────────
    REVENUE_BASE_CHOICES = [
        ('gross', 'درآمد ناخالص'),
        ('net',   'درآمد خالص'),
    ]
    REVENUE_PAYMENT_PERIOD_CHOICES = [
        ('weekly',    'هفتگی'),
        ('monthly',   'ماهانه'),
        ('quarterly', 'فصلی'),
    ]
    revenue_share_percentage = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        verbose_name='درصد سهم از درآمد'
    )
    revenue_share_base = models.CharField(
        max_length=10, choices=REVENUE_BASE_CHOICES,
        null=True, blank=True,
        verbose_name='مبنای محاسبه'
    )
    revenue_share_payment_period = models.CharField(
        max_length=20, choices=REVENUE_PAYMENT_PERIOD_CHOICES,
        null=True, blank=True,
        verbose_name='دوره پرداخت'
    )
    revenue_share_contract_duration = models.IntegerField(
        null=True, blank=True,
        verbose_name='مدت قرارداد (ماه)'
    )
    revenue_share_minimum_guarantee = models.DecimalField(
        max_digits=12, decimal_places=0,
        null=True, blank=True,
        verbose_name='حداقل تضمینی ماهانه'
    )

    # ── 5. فروش برند ──────────────────────────────────────────
    BRAND_LEGAL_STATUS_CHOICES = [
        ('registered',       'ثبت‌شده'),
        ('in_progress',      'در حال ثبت'),
        ('usage_right_only', 'فقط حق استفاده'),
    ]
    brand_transferred_assets = models.TextField(
        null=True, blank=True,
        verbose_name='اجزای برند منتقل‌شده'
    )
    brand_legal_status = models.CharField(
        max_length=25, choices=BRAND_LEGAL_STATUS_CHOICES,
        null=True, blank=True,
        verbose_name='وضعیت حقوقی برند'
    )
    brand_usage_restrictions = models.TextField(
        null=True, blank=True,
        verbose_name='محدودیت‌های کاربرد برند'
    )
    brand_industry_scope = models.CharField(
        max_length=300, null=True, blank=True,
        verbose_name='حوزه / صنعت برند'
    )

    # ═════════════════════════════════════════════════════════

    class Meta:
        ordering = ['-boost', '-premier', '-created_at']
        verbose_name = 'آگهی'
        verbose_name_plural = 'آگهی‌ها'

    def __str__(self):
        return self.title

    def has_access(self, user):
        if not self.is_private:
            return True
        if not user.is_authenticated:
            return False
        if user == self.seller:
            return True
        return self.visit_requests.filter(requester=user, status='approved').exists()

    def get_income_chart_data(self):
        income_points = self.income_data_points.all().order_by('date')
        return {
            'labels': [p.date.strftime('%Y/%m/%d') for p in income_points],
            'data':   [float(p.income) for p in income_points],
        }

    def get_views_chart_data(self):
        views_points = self.views_data_points.all().order_by('date')
        return {
            'labels': [p.date.strftime('%Y/%m/%d') for p in views_points],
            'data':   [p.views for p in views_points],
        }

    def get_final_price(self):
        return self.discount_price if self.discount_price else self.price

    def get_discount_percentage(self):
        if self.discount_price and self.price:
            return round(((self.price - self.discount_price) / self.price) * 100)
        return 0

    def calculate_roi(self):
        if self.avg_monthly_profit and self.get_final_price():
            return round((self.avg_monthly_profit / self.get_final_price()) * 100, 2)
        return 0

    def get_payback_period(self):
        if self.avg_monthly_profit and self.avg_monthly_profit > 0:
            return round(self.get_final_price() / self.avg_monthly_profit, 1)
        return None


# ── بقیه مدل‌ها بدون تغییر ───────────────────────────────────

class ListingAnalyst(models.Model):
    listing            = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name='listing_analyst', verbose_name='آگهی')
    analyst_name       = models.CharField(max_length=100, blank=True, verbose_name='نام تحلیلگر')
    analyst_expertise  = models.CharField(max_length=200, blank=True, verbose_name='تخصص')
    analyst_education  = models.CharField(max_length=200, blank=True, verbose_name='تحصیلات')
    analyst_record     = models.CharField(max_length=200, blank=True, verbose_name='سابقه')
    analyst_image      = models.ImageField(upload_to='analysts/', null=True, blank=True, verbose_name='تصویر تحلیلگر')
    analyst_description = models.TextField(blank=True, verbose_name='توضیحات تحلیلگر')

    class Meta:
        verbose_name = 'تحلیلگر'
        verbose_name_plural = 'تحلیلگران'

    def __str__(self):
        return f"تحلیلگر {self.listing.title}"


class SocialMedia(models.Model):
    PLATFORM_CHOICES = [
        ('twitter',   'توییتر'),
        ('instagram', 'اینستاگرام'),
        ('github',    'گیت‌هاب'),
        ('facebook',  'فیسبوک'),
        ('linkedin',  'لینکدین'),
        ('telegram',  'تلگرام'),
        ('other',     'سایر'),
    ]
    listing   = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='social_medias', verbose_name='آگهی')
    platform  = models.CharField(max_length=20, choices=PLATFORM_CHOICES, verbose_name='پلتفرم')
    followers = models.CharField(max_length=100, verbose_name='تعداد فالوور')
    url       = models.URLField(blank=True, verbose_name='لینک')

    class Meta:
        verbose_name = 'رسانه اجتماعی'
        verbose_name_plural = 'رسانه‌های اجتماعی'

    def __str__(self):
        return f"{self.get_platform_display()} - {self.followers}"


class Attachment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='attachments', verbose_name='آگهی')
    file    = models.FileField(upload_to='attachments/', verbose_name='فایل')

    class Meta:
        verbose_name = 'پیوست'
        verbose_name_plural = 'پیوست‌ها'

    def __str__(self):
        return self.file.name


class SaleInclude(models.Model):
    listing    = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='sale_includes', verbose_name='آگهی')
    asset_name = models.CharField(max_length=200, verbose_name='نام دارایی')

    class Meta:
        verbose_name = 'دارایی فروش'
        verbose_name_plural = 'دارایی‌های فروش'

    def __str__(self):
        return self.asset_name


class License(models.Model):
    listing      = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='licenses', verbose_name='آگهی')
    license_name = models.CharField(max_length=200, verbose_name='نام مجوز')

    class Meta:
        verbose_name = 'مجوز'
        verbose_name_plural = 'مجوزها'

    def __str__(self):
        return self.license_name


class ConfirmedInformation(models.Model):
    listing        = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='confirmed', verbose_name='آگهی')
    confirmed_name = models.CharField(max_length=200, verbose_name='نام اطلاعات تایید شده')

    class Meta:
        verbose_name = 'اطلاعات تایید'
        verbose_name_plural = 'اطلاعاتات تایید'

    def __str__(self):
        return self.confirmed_name


class ServiceUsed(models.Model):
    listing      = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='services_used', verbose_name='آگهی')
    service_name = models.CharField(max_length=200, verbose_name='نام خدمت')

    class Meta:
        verbose_name = 'خدمت مورد استفاده'
        verbose_name_plural = 'خدمات مورد استفاده'

    def __str__(self):
        return self.service_name


class MonetizationMethod(models.Model):
    METHOD_CHOICES = [
        ('banner_click_advertising',   'تبلیغات بنری و کلیکی'),
        ('sponsored_posts',            'پست‌های حمایت‌شده'),
        ('cooperation_sales',          'همکاری در فروش'),
        ('special_subscription_sale',  'فروش اشتراک ویژه'),
        ('selling_digital_products',   'فروش محصولات دیجیتال'),
        ('selling_physical_products',  'فروش محصولات فیزیکی'),
        ('receive_financial_support',  'دریافت حمایت مالی'),
        ('holding_training_courses',   'برگزاری دوره‌های آموزشی و وبینار'),
        ('sell_backlinks',             'فروش بک‌لینک و فضای تبلیغاتی'),
        ('providing_consulting_services', 'ارائه خدمات مشاوره و فریلنسری'),
    ]
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='monetization_methods', verbose_name='آگهی')
    method  = models.CharField(max_length=50, choices=METHOD_CHOICES, verbose_name='روش')

    class Meta:
        verbose_name = 'روش کسب درآمد'
        verbose_name_plural = 'روش‌های کسب درآمد'

    def __str__(self):
        return self.method


class Expense(models.Model):
    PERIOD_CHOICES = [
        ('monthly',  'ماهانه'),
        ('yearly',   'سالانه'),
        ('one_time', 'یکبار'),
    ]
    listing      = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='expenses', verbose_name='آگهی')
    expense_name = models.CharField(max_length=200, verbose_name='نام هزینه')
    amount       = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='مبلغ')
    period       = models.CharField(max_length=20, choices=PERIOD_CHOICES, verbose_name='دوره')

    class Meta:
        verbose_name = 'هزینه'
        verbose_name_plural = 'هزینه‌ها'

    def __str__(self):
        return f"{self.expense_name} - {self.amount}"


class IncomeDataPoint(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='income_data_points', verbose_name='آگهی')
    date    = models.DateField(verbose_name='تاریخ')
    income  = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='درآمد')

    class Meta:
        verbose_name = 'نقطه داده درآمد'
        verbose_name_plural = 'نقاط داده درآمد'
        ordering = ['date']
        unique_together = ['listing', 'date']

    def __str__(self):
        return f"{self.listing.title} - {self.date}: {self.income}"


class ViewsDataPoint(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='views_data_points', verbose_name='آگهی')
    date    = models.DateField(verbose_name='تاریخ')
    views   = models.IntegerField(verbose_name='بازدید')

    class Meta:
        verbose_name = 'نقطه داده بازدید'
        verbose_name_plural = 'نقاط داده بازدید'
        ordering = ['date']
        unique_together = ['listing', 'date']

    def __str__(self):
        return f"{self.listing.title} - {self.date}: {self.views}"


class ListingImage(models.Model):
    listing     = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image       = models.ImageField(upload_to='listings/gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"تصویر {self.listing.title}"


class VisitRequest(models.Model):
    STATUS_CHOICES = [
        ('pending',  'در انتظار تایید'),
        ('approved', 'تایید شده'),
        ('rejected', 'رد شده'),
    ]
    listing    = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='visit_requests')
    requester  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='visit_requests')
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message    = models.TextField(blank=True, verbose_name='پیام درخواست')
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
    listing     = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='income_proofs')
    image       = models.ImageField(upload_to='income_proofs/', verbose_name='تصویر اثبات درآمد', blank=True, null=True)
    description = models.TextField(blank=True, verbose_name='توضیحات')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'اثبات درآمد'
        verbose_name_plural = 'اثبات‌های درآمد'

    def __str__(self):
        return f"اثبات درآمد - {self.listing.title}"


class ListingFAQ(models.Model):
    listing  = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(blank=True, max_length=300, verbose_name='پرسش')
    answer   = models.TextField(blank=True, verbose_name='پاسخ')
    order    = models.PositiveIntegerField(blank=True, default=0, verbose_name='ترتیب')

    class Meta:
        verbose_name = 'پرسش و پاسخ'
        verbose_name_plural = 'پرسش‌ها و پاسخ‌ها'
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.listing.title} - {self.question}"


class TechnologyUsed(models.Model):
    TECHNOLOGY_CHOICES_CMS = [
        ('wordpress', 'وردپرس'), ('joomla', 'جوملا'), ('drupal', 'دروپال'),
        ('woocommerce', 'ووکامرس'), ('shopify', 'شاپیفای'), ('magento', 'مجنتو'),
        ('prestashop', 'پرستاشاپ'), ('opencart', 'اوپن‌کارت'), ('nopcommerce', 'ناپ‌کامرس'),
        ('strapi', 'استراپی'), ('contentful', 'کانتنت‌فول'), ('ghost', 'گوست'),
        ('sanity', 'سنتی'), ('custom_cms', 'سیستم اختصاصی'),
    ]
    TECHNOLOGY_CHOICES_BACKEND = [
        ('laravel', 'لاراول'), ('symfony', 'سیمفونی'), ('codeigniter', 'کدایگنایتر'),
        ('core_php', 'پی‌اچ‌پی خام'), ('nodejs', 'نود جی‌اس'), ('expressjs', 'اکسپرس'),
        ('nestjs', 'نست جی‌اس'), ('django', 'جنگو'), ('flask', 'فلسک'),
        ('fastapi', 'فست ای‌پی‌آی'), ('aspnet', 'ای‌اس‌پی دات‌نت کور'),
        ('springboot', 'اسپرینگ بوت'), ('golang', 'گو'), ('rails', 'روبی آن ریلز'), ('rust', 'راست'),
    ]
    TECHNOLOGY_CHOICES_FRONTEND = [
        ('reactjs', 'ری‌اکت'), ('nextjs', 'نکست جی‌اس'), ('vuejs', 'ویو جی‌اس'),
        ('nuxtjs', 'ناکس جی‌اس'), ('angular', 'انگولار'), ('svelte', 'سولت'),
        ('jquery', 'جی‌کوئری'), ('tailwind', 'تیلویند'), ('bootstrap', 'بوت‌استرپ'),
        ('mui', 'متریال یوآی'), ('antdesign', 'ان دیزاین'), ('sass_less', 'ساس/لس'),
        ('vite', 'ویت'), ('webpack', 'وب‌پک'),
    ]
    TECHNOLOGY_CHOICES_DATABASE = [
        ('mysql', 'مای‌اس‌کیوال'), ('postgresql', 'پستگرس‌کیوال'), ('mssql', 'مایکروسافت اس‌کیوال سرور'),
        ('sqlite', 'اس‌کیوال‌لایت'), ('oracle', 'اوراکل'), ('mongodb', 'مونگو دی‌بی'),
        ('cassandra', 'کاساندرا'), ('couchdb', 'کوچ‌دی‌بی'), ('firebase', 'فایربیس'),
        ('redis', 'ردیس'), ('memcached', 'مم‌کشد'), ('elasticsearch', 'الستیک‌سرچ'),
        ('algolia', 'آلگولیا'), ('solr', 'آپاچی سولر'),
    ]
    TECHNOLOGY_CHOICES_INFRASTRUCTURE = [
        ('shared_hosting', 'هاست اشتراکی'), ('vps', 'سرور مجازی'), ('dedicated', 'سرور اختصاصی'),
        ('hetzner', 'هتزنر'), ('digitalocean', 'دیجیتال اوشن'), ('aws', 'آمازون'),
        ('liara', 'لیارا'), ('arvancloud', 'آروان کلاد'), ('parspak', 'پارس‌پک'),
        ('nginx', 'انجین‌اکس'), ('apache', 'آپاچی'), ('litespeed', 'لایت‌اسپید'),
        ('iis', 'آی‌آی‌اس'), ('linux', 'لینوکس'), ('windows_server', 'ویندوز سرور'),
    ]
    TECHNOLOGY_CHOICES_MOBILE = [
        ('flutter', 'فلاتر'), ('react_native', 'ری‌اکت نیتیو'), ('ionic', 'آیونیک'),
        ('maui', '.NET MAUI'), ('android_native', 'اندروید بومی'), ('ios_native', 'آی‌او‌اس بومی'),
        ('pwa', 'پروگرسیو وب اپلیکیشن'),
    ]
    TECHNOLOGY_CHOICES_DEVOPS = [
        ('github', 'گیت‌هاب'), ('gitlab', 'گیت‌لب'), ('bitbucket', 'بیت‌باکت'),
        ('docker', 'داکر'), ('kubernetes', 'کوبرنیتیز'), ('github_actions', 'گیت‌هاب اکشنز'),
        ('gitlab_ci', 'گیت‌لب سی‌آی'), ('jenkins', 'جنکینز'),
    ]
    TECHNOLOGY_CHOICES_THIRD_PARTY = [
        ('zarinpal', 'زرین‌پال'), ('zibal', 'زیبال'), ('payping', 'پی‌پینگ'),
        ('bank_gateway', 'درگاه مستقیم بانکی'), ('kavenegar', 'کاوه‌نگار'),
        ('farazsms', 'فراز اس‌ام‌اس'), ('melipayamak', 'ملی‌پیامک'),
        ('mailchimp', 'میل‌چیمپ'), ('sender', 'سندر'), ('mailerlite', 'میلرلیت'),
        ('pocket', 'پاکت'), ('ga4', 'گوگل آنالیتیکس'), ('clarity', 'مایکروسافت کلریتی'),
        ('yandex_metrica', 'یاندکس متاریکا'),
    ]

    listing                  = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name='technologies_used', verbose_name='آگهی')
    technology_cms           = models.JSONField(default=list, blank=True, verbose_name='CMS و فروشگاه‌ساز')
    technology_backend       = models.JSONField(default=list, blank=True, verbose_name='تکنولوژی Backend')
    technology_frontend      = models.JSONField(default=list, blank=True, verbose_name='تکنولوژی Frontend')
    technology_database      = models.JSONField(default=list, blank=True, verbose_name='تکنولوژی Database')
    technology_infrastructure = models.JSONField(default=list, blank=True, verbose_name='تکنولوژی Infrastructure')
    technology_mobile        = models.JSONField(default=list, blank=True, verbose_name='تکنولوژی Mobile')
    technology_devops        = models.JSONField(default=list, blank=True, verbose_name='تکنولوژی DevOps')
    technology_third_party   = models.JSONField(default=list, blank=True, verbose_name='سرویس‌های جانبی')

    class Meta:
        verbose_name = 'تکنولوژی استفاده شده'
        verbose_name_plural = 'تکنولوژی‌های استفاده شده'

    def __str__(self):
        return f"تکنولوژی‌های آگهی: {self.listing.title}"

    def _display_list(self, choices, values):
        lookup = dict(choices)
        return [lookup.get(v, v) for v in values]

    def get_cms_display_list(self):           return self._display_list(self.TECHNOLOGY_CHOICES_CMS,            self.technology_cms)
    def get_backend_display_list(self):       return self._display_list(self.TECHNOLOGY_CHOICES_BACKEND,        self.technology_backend)
    def get_frontend_display_list(self):      return self._display_list(self.TECHNOLOGY_CHOICES_FRONTEND,       self.technology_frontend)
    def get_database_display_list(self):      return self._display_list(self.TECHNOLOGY_CHOICES_DATABASE,       self.technology_database)
    def get_infrastructure_display_list(self):return self._display_list(self.TECHNOLOGY_CHOICES_INFRASTRUCTURE, self.technology_infrastructure)
    def get_mobile_display_list(self):        return self._display_list(self.TECHNOLOGY_CHOICES_MOBILE,         self.technology_mobile)
    def get_devops_display_list(self):        return self._display_list(self.TECHNOLOGY_CHOICES_DEVOPS,         self.technology_devops)
    def get_third_party_display_list(self):   return self._display_list(self.TECHNOLOGY_CHOICES_THIRD_PARTY,    self.technology_third_party)


class TrafficSource(models.Model):
    SOURCE_CHOICES = [
        ('organic_search',    'جستجوی ارگانیک (SEO)'),
        ('direct',            'ترافیک مستقیم'),
        ('social_media',      'شبکه‌های اجتماعی'),
        ('referral',          'ارجاعی'),
        ('paid_ads',          'تبلیغات پولی'),
        ('email_sms',         'ایمیل مارکتینگ و پیامک'),
        ('push_notification', 'پوش نوتیفیکیشن'),
    ]
    listing    = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='traffic_sources', verbose_name='آگهی')
    source     = models.CharField(max_length=30, choices=SOURCE_CHOICES, verbose_name='منبع')
    percentage = models.PositiveSmallIntegerField(verbose_name='درصد')

    class Meta:
        verbose_name = 'منبع ترافیک'
        verbose_name_plural = 'منابع ترافیک'
        unique_together = ['listing', 'source']

    def __str__(self):
        return f"{self.get_source_display()} - {self.percentage}%"