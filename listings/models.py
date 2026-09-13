# listings/models.py



from django.db import models
from django.conf import settings


class Category(models.Model):
    # ═══════ دسته‌بندی اصلی + زیرمجموعه (نوع دارایی دیجیتال) ═══════
    PLATFORM_CATEGORIES = [
        ('website', 'وب‌سایت', [
            ('website_blog', 'وبلاگ / بلاگ محتوایی'),
            ('website_news_magazine', 'خبری و مجله آنلاین'),
            ('website_forum_community', 'انجمن و جامعه آنلاین (فروم)'),
            ('website_directory', 'دایرکتوری و نیازمندی'),
            ('website_portal', 'پرتال چندمنظوره'),
            ('website_review', 'وبسایت بررسی و ریویو'),
            ('website_landing_page', 'لندینگ پیج / صفحه فروش'),
            ('website_corporate', 'وبسایت شرکتی و معرفی کسب‌وکار'),
            ('website_educational', 'وبسایت آموزشی / دوره آنلاین'),
            ('website_job_board', 'کاریابی و آگهی استخدام'),
            ('website_dating', 'وبسایت آشنایی و دوستیابی'),
            ('website_real_estate', 'وبسایت آگهی املاک'),
            ('website_classifieds', 'وبسایت نیازمندی و آگهی عمومی'),
            ('website_other', 'سایر وبسایت‌ها'),
        ]),
        ('ecommerce', 'فروشگاه اینترنتی', [
            ('ecommerce_woocommerce', 'فروشگاه ووکامرس (WordPress)'),
            ('ecommerce_shopify', 'فروشگاه شاپیفای'),
            ('ecommerce_opencart_prestashop', 'فروشگاه اوپن‌کارت / پرستاشاپ'),
            ('ecommerce_custom', 'فروشگاه با کدنویسی اختصاصی'),
            ('ecommerce_marketplace_shop', 'فروشگاه داخل مارکت‌پلیس (دیجی‌کالا، باسلام و ...)'),
            ('ecommerce_dropship', 'فروشگاه دراپ‌شیپینگ'),
            ('ecommerce_digital_products', 'فروش محصولات دیجیتال'),
            ('ecommerce_physical_products', 'فروش محصولات فیزیکی'),
            ('ecommerce_subscription_box', 'اشتراک دوره‌ای محصول (Subscription Box)'),
            ('ecommerce_other', 'سایر فروشگاه‌های اینترنتی'),
        ]),
        ('app', 'اپلیکیشن', [
            ('app_android', 'اپلیکیشن اندروید'),
            ('app_ios', 'اپلیکیشن iOS'),
            ('app_cross_platform', 'اپلیکیشن کراس‌پلتفرم (Flutter / React Native)'),
            ('app_pwa', 'وب‌اپلیکیشن (PWA)'),
            ('app_desktop', 'نرم‌افزار دسکتاپ'),
            ('app_game_mobile', 'بازی موبایل'),
            ('app_game_pc_console', 'بازی PC / کنسول'),
            ('app_saas', 'اپلیکیشن / سرویس SaaS'),
            ('app_browser_extension', 'اکستنشن مرورگر'),
            ('app_telegram_bot', 'ربات تلگرام'),
            ('app_other', 'سایر اپلیکیشن‌ها'),
        ]),
        ('social_media', 'شبکه‌های اجتماعی', [
            ('social_instagram', 'پیج اینستاگرام'),
            ('social_telegram_channel', 'کانال تلگرام'),
            ('social_telegram_group', 'گروه تلگرام'),
            ('social_youtube', 'کانال یوتیوب'),
            ('social_aparat', 'کانال آپارات'),
            ('social_twitter_x', 'پیج توییتر / X'),
            ('social_facebook', 'پیج فیسبوک'),
            ('social_linkedin', 'پیج لینکدین'),
            ('social_tiktok', 'پیج تیک‌تاک'),
            ('social_pinterest', 'پیج پینترست'),
            ('social_threads', 'پیج تردز (Threads)'),
            ('social_clubhouse', 'اکانت کلاب‌هاوس'),
            ('social_other', 'سایر شبکه‌های اجتماعی'),
        ]),
        ('content_media', 'رسانه و محتوا', [
            ('content_podcast', 'پادکست'),
            ('content_newsletter', 'خبرنامه ایمیلی (Newsletter)'),
            ('content_adsense_channel', 'کانال درآمد از تبلیغات (AdSense / YPP)'),
            ('content_streaming', 'سرویس پخش زنده / استریمینگ'),
            ('content_ebook_course', 'کتاب الکترونیک و دوره ضبط‌شده'),
            ('content_stock_media', 'فروش عکس/ویدیو استوک'),
            ('content_other', 'سایر محتوا و رسانه'),
        ]),
        ('domain', 'دامنه', [
            ('domain_com', 'دامنه .com'),
            ('domain_ir', 'دامنه .ir'),
            ('domain_international_other', 'سایر دامنه‌های بین‌المللی (.net, .org, ...)'),
            ('domain_brandable', 'دامنه برندی / کوتاه'),
            ('domain_keyword', 'دامنه کلمه کلیدی (Exact Match)'),
            ('domain_portfolio', 'مجموعه دامنه (Domain Portfolio)'),
        ]),
        ('service_business', 'کسب‌وکار خدماتی آنلاین', [
            ('service_agency', 'آژانس / تیم خدماتی (طراحی، سئو، مارکتینگ)'),
            ('service_freelance_platform', 'پلتفرم فریلنسری'),
            ('service_consulting', 'مشاوره و کوچینگ آنلاین'),
            ('service_membership_site', 'سایت عضویت / اشتراک ویژه'),
            ('service_marketplace', 'مارکت‌پلیس واسط خرید و فروش'),
            ('service_booking', 'سیستم رزرو و نوبت‌دهی آنلاین'),
            ('service_other', 'سایر کسب‌وکارهای خدماتی'),
        ]),
        ('other', 'سایر', [
            ('other_misc', 'متفرقه'),
        ]),
    ]

    # فلت‌شده برای استفاده در فیلد مدل (choices)
    PLATFORM_CHOICES = [
        (sub_slug, sub_label)
        for _, _, subs in PLATFORM_CATEGORIES
        for sub_slug, sub_label in subs
    ]

    name = models.CharField(max_length=100, verbose_name='نام')
    platform = models.CharField(max_length=40, choices=PLATFORM_CHOICES, verbose_name='نوع پلتفرم (زیرمجموعه)')
    description = models.TextField(blank=True, verbose_name='توضیحات')

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'

    def __str__(self):
        return f"{self.name} ({self.get_platform_display()})"

    def get_platform_display_safe(self):
        """
        نمایش برچسب فارسیِ پلتفرم، حتی اگر به‌جای اسلاگ زیردسته،
        اسلاگ دسته‌ی اصلی ذخیره شده باشد (fallback امن).
        """
        choices_dict = dict(self.PLATFORM_CHOICES)
        if self.platform in choices_dict:
            return choices_dict[self.platform]

        # اگر مقدار ذخیره‌شده یک "دسته اصلی" باشد نه زیردسته
        for slug, label, subs in self.PLATFORM_CATEGORIES:
            if slug == self.platform:
                return label

        # آخرین راه: خود مقدار خام را برگردان تا صفحه نشکند
        return self.platform

    def get_platform_main_category(self):
        """برگرداندن (slug, label) دسته کلیِ این دسته‌بندی"""
        for slug, label, subs in self.PLATFORM_CATEGORIES:
            if any(sub_slug == self.platform for sub_slug, _ in subs):
                return slug, label
        return None, None

    @classmethod
    def get_platform_category_map(cls):
        """نگاشت هر زیرمجموعه به دسته کلی خودش"""
        mapping = {}
        for slug, label, subs in cls.PLATFORM_CATEGORIES:
            for sub_slug, sub_label in subs:
                mapping[sub_slug] = (slug, label)
        return mapping

class Listing(models.Model):

    # ─── وضعیت ───────────────────────────────────────────────
    STATUS_CHOICES = [
        ('pending',  'در انتظار تایید'),
        ('active',   'فعال'),
        ('sold',     'فروخته شده'),
        ('rejected', 'رد شده'),
        ('deleted',  'حذف شده'),
    ]

    # ─── حوزه فعالیت (دسته کلی + زیرمجموعه، الگوبرداری از Flippa) ─────
    ACTIVITY_CATEGORIES = [
        ('automotive', 'خودرو و وسایل نقلیه', [
            ('automotive_cars', 'خودرو'),
            ('automotive_motorcycles', 'موتورسیکلت'),
            ('automotive_other', 'سایر خودرویی'),
        ]),
        ('business', 'کسب‌وکار', [
            ('business_finance', 'مالی'),
            ('business_forex', 'فارکس'),
            ('business_insurance', 'بیمه'),
            ('business_jobs', 'استخدام و کاریابی'),
            ('business_law', 'حقوقی'),
            ('business_productivity', 'بهره‌وری و مدیریت'),
            ('business_real_estate', 'املاک و مستغلات'),
            ('business_sales_marketing', 'فروش و بازاریابی'),
            ('business_shopping', 'خرید و فروشگاهی'),
            ('business_other', 'سایر کسب‌وکار'),
        ]),
        ('technology', 'فناوری و نرم‌افزار', [
            ('tech_saas', 'سرویس ابری و SaaS'),
            ('tech_apps', 'اپلیکیشن و موبایل'),
            ('tech_ai', 'هوش مصنوعی'),
            ('tech_cybersecurity', 'امنیت سایبری'),
            ('tech_blockchain_crypto', 'بلاک‌چین و ارز دیجیتال'),
            ('tech_dev_tools', 'ابزارهای توسعه‌دهندگان'),
            ('tech_other', 'سایر فناوری'),
        ]),
        ('design_style', 'طراحی و سبک', [
            ('design_art', 'هنر'),
            ('design_fashion', 'مد و فشن'),
            ('design_jewelry', 'جواهرات'),
            ('design_logos', 'طراحی لوگو'),
            ('design_photography', 'عکاسی'),
            ('design_tattoos', 'تتو'),
            ('design_other', 'سایر طراحی و سبک'),
        ]),
        ('education', 'آموزش', [
            ('education_colleges_courses', 'دانشگاه و دوره‌های آموزشی'),
            ('education_languages', 'آموزش زبان'),
            ('education_scholarships', 'بورسیه تحصیلی'),
            ('education_guides_tutorials', 'راهنما و آموزش‌های تخصصی'),
            ('education_other', 'سایر آموزشی'),
        ]),
        ('electronics', 'الکترونیک', [
            ('electronics_cameras', 'دوربین'),
            ('electronics_mobile', 'موبایل'),
            ('electronics_computers', 'کامپیوتر'),
            ('electronics_tablets', 'تبلت و ای‌ریدر'),
            ('electronics_tv', 'تلویزیون'),
            ('electronics_other', 'سایر الکترونیک'),
        ]),
        ('entertainment', 'سرگرمی و رسانه', [
            ('entertainment_books', 'کتاب'),
            ('entertainment_celebrities', 'سلبریتی‌ها'),
            ('entertainment_events', 'رویدادها'),
            ('entertainment_film', 'فیلم و سینما'),
            ('entertainment_humor', 'طنز و سرگرمی'),
            ('entertainment_music', 'موسیقی'),
            ('entertainment_tv', 'تلویزیون و سریال'),
            ('entertainment_other', 'سایر سرگرمی'),
        ]),
        ('food_drink', 'غذا و نوشیدنی', [
            ('food_cooking_recipes', 'آشپزی و دستور پخت'),
            ('food_drinks', 'نوشیدنی'),
            ('food_general', 'غذا'),
            ('food_other', 'سایر غذا و نوشیدنی'),
        ]),
        ('general_knowledge', 'دانش عمومی', [
            ('gk_news_affairs', 'اخبار و رویدادهای جاری'),
            ('gk_politics_history', 'سیاست و تاریخ'),
            ('gk_religion_spirituality', 'مذهب و معنویت'),
            ('gk_science_nature', 'علم و طبیعت'),
            ('gk_other', 'سایر دانش عمومی'),
        ]),
        ('health_beauty', 'سلامت و زیبایی', [
            ('health_beauty_general', 'زیبایی'),
            ('health_bodybuilding', 'بدنسازی'),
            ('health_mental', 'افسردگی و اضطراب'),
            ('health_diet_nutrition', 'رژیم و تغذیه'),
            ('health_fitness', 'تناسب اندام'),
            ('health_hair', 'مو و ریزش مو'),
            ('health_medical', 'پزشکی'),
            ('health_pregnancy', 'بارداری'),
            ('health_skin', 'پوست'),
            ('health_sleep', 'خواب و خروپف'),
            ('health_smoking', 'ترک سیگار'),
            ('health_teeth', 'دندان'),
            ('health_weight_loss', 'کاهش وزن'),
            ('health_other', 'سایر سلامت و زیبایی'),
        ]),
        ('hobbies_games', 'سرگرمی‌ها و بازی', [
            ('hobbies_gambling', 'شرط‌بندی'),
            ('hobbies_board_games', 'بازی‌های فکری'),
            ('hobbies_gaming', 'گیمینگ'),
            ('hobbies_other', 'سایر سرگرمی‌ها'),
        ]),
        ('home_garden', 'خانه و باغ', [
            ('home_diy', 'کارهای دستی (DIY)'),
            ('home_furniture', 'مبلمان'),
            ('home_gardening', 'باغبانی'),
            ('home_pets', 'حیوانات خانگی'),
            ('home_toys', 'اسباب‌بازی'),
            ('home_other', 'سایر خانه و باغ'),
        ]),
        ('internet', 'اینترنت و آنلاین', [
            ('internet_auctions', 'حراجی آنلاین'),
            ('internet_coupons_deals', 'تخفیف و کوپن'),
            ('internet_domaining', 'دامنه و دامنه‌داری'),
            ('internet_marketing', 'بازاریابی اینترنتی'),
            ('internet_community', 'انجمن و جامعه آنلاین'),
            ('internet_seo', 'سئو'),
            ('internet_social_media', 'شبکه‌های اجتماعی'),
            ('internet_traffic', 'جذب ترافیک'),
            ('internet_web_dev', 'وب دولوپمنت'),
            ('internet_web_design', 'طراحی وب‌سایت'),
            ('internet_other', 'سایر اینترنتی'),
        ]),
        ('lifestyle', 'سبک زندگی', [
            ('lifestyle_baby', 'نوزاد'),
            ('lifestyle_children', 'کودکان'),
            ('lifestyle_dating', 'آشنایی و دوستیابی'),
            ('lifestyle_wedding', 'عروسی'),
            ('lifestyle_other', 'سایر سبک زندگی'),
        ]),
        ('sports_outdoor', 'ورزش و فضای باز', [
            ('sports_boating', 'قایقرانی'),
            ('sports_camping', 'کمپینگ'),
            ('sports_cycling', 'دوچرخه‌سواری'),
            ('sports_football', 'فوتبال'),
            ('sports_golf', 'گلف'),
            ('sports_hunting', 'شکار'),
            ('sports_other', 'سایر ورزشی'),
        ]),
        ('travel', 'سفر و گردشگری', [
            ('travel_flights_aviation', 'پرواز و هوانوردی'),
            ('travel_guides', 'راهنمای سفر'),
            ('travel_hotels', 'هتل'),
            ('travel_vacation_resorts', 'تعطیلات و تفریح'),
            ('travel_other', 'سایر سفر'),
        ]),
    ]

    # فلت‌شده برای استفاده در فیلد مدل (choices)
    ACTIVITY_CHOICES = [
        (sub_slug, sub_label)
        for _, _, subs in ACTIVITY_CATEGORIES
        for sub_slug, sub_label in subs
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

    category = models.CharField(max_length=40, choices=Category.PLATFORM_CHOICES,
                                null=True, blank=True, verbose_name='دسته‌بندی')
    asset_details = models.JSONField(default=dict, blank=True, verbose_name='اطلاعات اختصاصی دارایی')
    title       = models.CharField(max_length=200, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    location    = models.CharField(max_length=200, null=True, blank=True, verbose_name='موقعیت')
    price          = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='قیمت')
    discount_price = models.DecimalField(max_digits=12, decimal_places=0,
                                         null=True, blank=True, verbose_name='قیمت با تخفیف')
    about_platform = models.TextField(null=True, blank=True, verbose_name='درباره پلتفرم')

    platform_url    = models.URLField(blank=True, verbose_name='آدرس پلتفرم')
    followers_count = models.IntegerField(default=0, blank=True, verbose_name='تعداد کاربر ها')
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

    areas_activity = models.CharField(max_length=60, choices=ACTIVITY_CHOICES, verbose_name='حوزه‌ فعالیت')

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

    def get_category_display_safe(self):
        """
        نمایش برچسب فارسیِ دسته‌بندی پلتفرم، حتی اگر به‌جای اسلاگ زیردسته،
        اسلاگ دسته‌ی اصلی ذخیره شده باشد (fallback امن).
        """
        choices_dict = dict(Category.PLATFORM_CHOICES)
        if self.category in choices_dict:
            return choices_dict[self.category]

        # اگر مقدار ذخیره‌شده یک "دسته اصلی" باشد نه زیردسته
        for slug, label, subs in Category.PLATFORM_CATEGORIES:
            if slug == self.category:
                return label

        return self.category or ''

    def get_areas_activity_display_safe(self):
        """
        نمایش برچسب فارسیِ حوزه فعالیت، حتی اگر اسلاگ دسته‌ی اصلی
        (نه زیردسته) ذخیره شده باشد.
        """
        choices_dict = dict(self.ACTIVITY_CHOICES)
        if self.areas_activity in choices_dict:
            return choices_dict[self.areas_activity]

        for slug, label, subs in self.ACTIVITY_CATEGORIES:
            if slug == self.areas_activity:
                return label

        return self.areas_activity

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

    def get_activity_main_category(self):
        """برگرداندن (slug, label) دسته کلیِ حوزه فعالیت این آگهی"""
        for slug, label, subs in self.ACTIVITY_CATEGORIES:
            if any(sub_slug == self.areas_activity for sub_slug, _ in subs):
                return slug, label
        return None, None

    @classmethod
    def get_activity_category_map(cls):
        """نگاشت هر زیرمجموعه به دسته کلی خودش، برای استفاده سریع در ویو/تمپلیت"""
        mapping = {}
        for slug, label, subs in cls.ACTIVITY_CATEGORIES:
            for sub_slug, sub_label in subs:
                mapping[sub_slug] = (slug, label)
        return mapping


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




# ═══════════════════════════════════════════════════════════════
#  مدل‌های اختصاصی دسته‌بندی
#  هر آگهی حداکثر یکی از این‌ها را دارد (بسته به category)
# ═══════════════════════════════════════════════════════════════


class WebsiteDetails(models.Model):
    """جزئیات اختصاصی وب‌سایت."""
    listing = models.OneToOneField(
        Listing, on_delete=models.CASCADE,
        related_name='website_details', verbose_name='آگهی'
    )

    tech_stack           = models.CharField(max_length=300, blank=True, verbose_name='تکنولوژی‌های سایت')
    monthly_visits       = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='بازدید ماهانه')
    unique_visitors      = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='کاربران یکتای ماهانه')
    page_views           = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='بازدید صفحات ماهانه')
    pages_indexed        = models.PositiveIntegerField(null=True, blank=True, verbose_name='صفحات ایندکس‌شده گوگل')
    domain_authority     = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Domain Authority')
    backlinks_count      = models.PositiveIntegerField(null=True, blank=True, verbose_name='تعداد بک‌لینک')
    content_count        = models.PositiveIntegerField(null=True, blank=True, verbose_name='تعداد مقالات / پست‌ها')
    seo_score            = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='امتیاز سئو (0-100)')
    bounce_rate          = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='نرخ پرش (%)')
    avg_session_duration = models.PositiveIntegerField(null=True, blank=True, verbose_name='میانگین مدت بازدید (ثانیه)')

    class Meta:
        verbose_name = 'جزئیات وب‌سایت'
        verbose_name_plural = 'جزئیات وب‌سایت‌ها'

    def __str__(self):
        return f"وب‌سایت: {self.listing.title}"


class EcommerceDetails(models.Model):
    """جزئیات اختصاصی فروشگاه اینترنتی."""
    listing = models.OneToOneField(
        Listing, on_delete=models.CASCADE,
        related_name='ecommerce_details', verbose_name='آگهی'
    )

    products_count       = models.PositiveIntegerField(null=True, blank=True, verbose_name='تعداد محصولات')
    orders_per_month     = models.PositiveIntegerField(null=True, blank=True, verbose_name='سفارش ماهانه')
    aov                  = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='میانگین ارزش سفارش (تومان)')
    conversion_rate      = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='نرخ تبدیل (%)')
    returning_customers  = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='مشتریان بازگشتی (%)')
    shipping_partners    = models.CharField(max_length=300, blank=True, verbose_name='شرکت‌های حمل‌ونقل')
    inventory_value      = models.DecimalField(max_digits=14, decimal_places=0, null=True, blank=True, verbose_name='ارزش موجودی انبار (تومان)')
    cart_abandonment     = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='نرخ رهاسازی سبد (%)')
    suppliers_count      = models.PositiveIntegerField(null=True, blank=True, verbose_name='تعداد تامین‌کنندگان')
    has_inventory        = models.BooleanField(default=False, verbose_name='دارای انبار فعال')

    class Meta:
        verbose_name = 'جزئیات فروشگاه'
        verbose_name_plural = 'جزئیات فروشگاه‌ها'

    def __str__(self):
        return f"فروشگاه: {self.listing.title}"


class AppDetails(models.Model):
    """جزئیات اختصاصی اپلیکیشن."""
    listing = models.OneToOneField(
        Listing, on_delete=models.CASCADE,
        related_name='app_details', verbose_name='آگهی'
    )

    downloads            = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='تعداد کل دانلود')
    active_installs      = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='نصب‌های فعال')
    dau                  = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='کاربران فعال روزانه')
    mau                  = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='کاربران فعال ماهانه')
    rating               = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, verbose_name='امتیاز (از ۵)')
    reviews_count        = models.PositiveIntegerField(null=True, blank=True, verbose_name='تعداد نظرات')
    retention_rate       = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='نرخ نگهداشت (%)')
    current_version      = models.CharField(max_length=50, blank=True, verbose_name='نسخه فعلی')
    last_update_date     = models.CharField(max_length=50, blank=True, verbose_name='آخرین بروزرسانی')
    has_in_app_purchase  = models.BooleanField(default=False, verbose_name='خرید درون‌برنامه‌ای')
    crash_rate           = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='نرخ کرش (%)')

    class Meta:
        verbose_name = 'جزئیات اپلیکیشن'
        verbose_name_plural = 'جزئیات اپلیکیشن‌ها'

    def __str__(self):
        return f"اپلیکیشن: {self.listing.title}"


class SocialMediaDetails(models.Model):
    """جزئیات اختصاصی پیج/کانال شبکه اجتماعی."""
    listing = models.OneToOneField(
        Listing, on_delete=models.CASCADE,
        related_name='social_details', verbose_name='آگهی'
    )

    handle             = models.CharField(max_length=100, blank=True, verbose_name='نام کاربری / Handle')
    followers          = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='تعداد فالوور')
    following          = models.PositiveIntegerField(null=True, blank=True, verbose_name='تعداد Following')
    posts_count        = models.PositiveIntegerField(null=True, blank=True, verbose_name='تعداد پست‌ها')
    engagement_rate    = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='نرخ تعامل (%)')
    avg_reach          = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='میانگین ریچ هر پست')
    avg_story_views    = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='میانگین بازدید استوری')
    post_frequency     = models.PositiveIntegerField(null=True, blank=True, verbose_name='تعداد پست در هفته')
    audience_country   = models.CharField(max_length=100, blank=True, verbose_name='کشور اصلی مخاطبان')
    audience_gender    = models.CharField(max_length=50, blank=True, verbose_name='جنسیت غالب مخاطبان')
    audience_age_range = models.CharField(max_length=50, blank=True, verbose_name='بازه سنی مخاطبان')
    is_monetized       = models.BooleanField(default=False, verbose_name='مونتیزه شده')
    has_verification   = models.BooleanField(default=False, verbose_name='دارای تیک آبی')

    class Meta:
        verbose_name = 'جزئیات پیج/کانال'
        verbose_name_plural = 'جزئیات پیج‌ها/کانال‌ها'

    def __str__(self):
        return f"پیج: {self.listing.title}"


class ContentMediaDetails(models.Model):
    """جزئیات اختصاصی رسانه و محتوا."""
    listing = models.OneToOneField(
        Listing, on_delete=models.CASCADE,
        related_name='content_details', verbose_name='آگهی'
    )

    CONTENT_TYPE_CHOICES = [
        ('podcast',    'پادکست'),
        ('newsletter', 'خبرنامه ایمیلی'),
        ('youtube',    'کانال یوتیوب'),
        ('blog',       'وبلاگ محتوایی'),
        ('video',      'ویدیویی'),
        ('ebook',      'کتاب الکترونیک'),
        ('course',     'دوره آموزشی'),
        ('other',      'سایر'),
    ]

    content_type         = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, blank=True, verbose_name='نوع محتوا')
    subscribers          = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='تعداد مشترکین')
    monthly_audience     = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='مخاطبان ماهانه')
    episodes_count       = models.PositiveIntegerField(null=True, blank=True, verbose_name='تعداد قسمت‌ها/شماره‌ها')
    publishing_frequency = models.CharField(max_length=50, blank=True, verbose_name='دوره انتشار')
    avg_engagement       = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='میانگین تعامل هر قسمت')
    platforms            = models.CharField(max_length=300, blank=True, verbose_name='پلتفرم‌های انتشار')
    avg_downloads        = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='میانگین دانلود/پخش هر قسمت')
    open_rate            = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='نرخ باز شدن ایمیل (%)')
    click_rate           = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='نرخ کلیک (%)')

    class Meta:
        verbose_name = 'جزئیات رسانه'
        verbose_name_plural = 'جزئیات رسانه‌ها'

    def __str__(self):
        return f"رسانه: {self.listing.title}"


class DomainDetails(models.Model):
    """جزئیات اختصاصی دامنه."""
    listing = models.OneToOneField(
        Listing, on_delete=models.CASCADE,
        related_name='domain_details', verbose_name='آگهی'
    )

    domain_name       = models.CharField(max_length=255, blank=True, verbose_name='نام دامنه', db_index=True)
    extension         = models.CharField(max_length=20, blank=True, verbose_name='پسوند')
    registrar         = models.CharField(max_length=200, blank=True, verbose_name='ثبت‌کننده (Registrar)')
    expiry_date       = models.DateField(null=True, blank=True, verbose_name='تاریخ انقضا')
    domain_age_years  = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name='سن دامنه (سال)')
    monthly_type_in   = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='ترافیک تایپ-این ماهانه')
    backlinks_count   = models.PositiveIntegerField(null=True, blank=True, verbose_name='تعداد بک‌لینک')
    keyword           = models.CharField(max_length=200, blank=True, verbose_name='کلمه کلیدی اصلی')
    search_volume     = models.PositiveIntegerField(null=True, blank=True, verbose_name='حجم جستجوی ماهانه')
    cpc               = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name='CPC کلمه کلیدی (تومان)')
    is_brandable      = models.BooleanField(default=False, verbose_name='برندی / کوتاه')
    is_exact_match    = models.BooleanField(default=False, verbose_name='Exact Match Domain')
    has_history       = models.BooleanField(default=False, verbose_name='سابقه سایت قبلی دارد')

    class Meta:
        verbose_name = 'جزئیات دامنه'
        verbose_name_plural = 'جزئیات دامنه‌ها'

    def __str__(self):
        return f"دامنه: {self.domain_name or self.listing.title}"


class ServiceBusinessDetails(models.Model):
    """جزئیات اختصاصی کسب‌وکار خدماتی آنلاین."""
    listing = models.OneToOneField(
        Listing, on_delete=models.CASCADE,
        related_name='service_details', verbose_name='آگهی'
    )

    services_list         = models.TextField(blank=True, verbose_name='خدمات ارائه‌شده')
    team_size             = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='اندازه تیم')
    active_clients        = models.PositiveIntegerField(null=True, blank=True, verbose_name='مشتریان فعال')
    total_clients         = models.PositiveIntegerField(null=True, blank=True, verbose_name='کل مشتریان')
    avg_project_value     = models.DecimalField(max_digits=14, decimal_places=0, null=True, blank=True, verbose_name='میانگین ارزش پروژه (تومان)')
    monthly_projects      = models.PositiveIntegerField(null=True, blank=True, verbose_name='تعداد پروژه در ماه')
    client_retention      = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='نرخ حفظ مشتری (%)')
    contracts_count       = models.PositiveIntegerField(null=True, blank=True, verbose_name='قراردادهای فعال')
    recurring_revenue_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='درصد درآمد تکرارشونده (%)')
    has_registered_brand  = models.BooleanField(default=False, verbose_name='برند ثبت‌شده دارد')
    has_physical_office   = models.BooleanField(default=False, verbose_name='دفتر فیزیکی دارد')

    class Meta:
        verbose_name = 'جزئیات کسب‌وکار خدماتی'
        verbose_name_plural = 'جزئیات کسب‌وکارهای خدماتی'

    def __str__(self):
        return f"کسب‌وکار: {self.listing.title}"