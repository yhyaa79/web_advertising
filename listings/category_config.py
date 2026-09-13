# listings/category_config.py
# ═══════════════════════════════════════════════════════════════
#  کانفیگ مرکزی فرم ثبت آگهی بر اساس دسته‌بندی اصلی
# ═══════════════════════════════════════════════════════════════

# ─── فیلدهای اختصاصی هر دسته (در Listing.asset_details ذخیره می‌شوند) ───
CATEGORY_FORM_CONFIG = {
    'website': {
        'label': 'وب‌سایت',
        'icon': '🌐',
        'title': 'اطلاعات اختصاصی وب‌سایت',
        'fields': [
            {'name': 'tech_stack',        'label': 'تکنولوژی‌های سایت',         'type': 'text',     'placeholder': 'مثال: WordPress + WooCommerce'},
            {'name': 'monthly_visits',    'label': 'بازدید ماهانه',              'type': 'number'},
            {'name': 'unique_visitors',   'label': 'کاربران یکتای ماهانه',       'type': 'number'},
            {'name': 'pages_indexed',     'label': 'صفحات ایندکس‌شده در گوگل',   'type': 'number'},
            {'name': 'domain_authority',  'label': 'Domain Authority (DA)',     'type': 'number'},
            {'name': 'backlinks_count',   'label': 'تعداد بک‌لینک',              'type': 'number'},
            {'name': 'content_count',     'label': 'تعداد مقالات / پست‌ها',      'type': 'number'},
            {'name': 'seo_score',         'label': 'امتیاز سئو (0-100)',         'type': 'number'},
            {'name': 'bounce_rate',       'label': 'نرخ پرش (%)',                'type': 'number'},
        ]
    },

    'ecommerce': {
        'label': 'فروشگاه اینترنتی',
        'icon': '🛒',
        'title': 'اطلاعات اختصاصی فروشگاه',
        'fields': [
            {'name': 'products_count',         'label': 'تعداد محصولات',                'type': 'number'},
            {'name': 'orders_per_month',       'label': 'سفارش ماهانه',                  'type': 'number'},
            {'name': 'aov',                    'label': 'میانگین ارزش سفارش (تومان)',   'type': 'number'},
            {'name': 'conversion_rate',        'label': 'نرخ تبدیل (%)',                 'type': 'number'},
            {'name': 'returning_customers',    'label': 'درصد مشتریان بازگشتی (%)',      'type': 'number'},
            {'name': 'shipping_partners',      'label': 'شرکت‌های حمل‌ونقل',              'type': 'text',  'placeholder': 'پست، تیپاکس، ماهکس...'},
            {'name': 'inventory_value',        'label': 'ارزش موجودی انبار (تومان)',     'type': 'number'},
            {'name': 'cart_abandonment',       'label': 'نرخ رهاسازی سبد خرید (%)',      'type': 'number'},
        ]
    },

    'app': {
        'label': 'اپلیکیشن',
        'icon': '📱',
        'title': 'اطلاعات اختصاصی اپلیکیشن',
        'fields': [
            {'name': 'downloads',              'label': 'تعداد کل دانلود',           'type': 'number'},
            {'name': 'dau',                    'label': 'کاربران فعال روزانه (DAU)', 'type': 'number'},
            {'name': 'mau',                    'label': 'کاربران فعال ماهانه (MAU)','type': 'number'},
            {'name': 'rating',                 'label': 'امتیاز (از ۵)',             'type': 'number', 'step': '0.1'},
            {'name': 'reviews_count',          'label': 'تعداد نظرات',               'type': 'number'},
            {'name': 'retention_rate',         'label': 'نرخ نگهداشت کاربر (%)',     'type': 'number'},
            {'name': 'current_version',        'label': 'نسخه فعلی',                 'type': 'text'},
            {'name': 'last_update',            'label': 'آخرین بروزرسانی',           'type': 'text',  'placeholder': 'مثال: ۱۴۰۳/۰۸'},
            {'name': 'has_in_app_purchase',    'label': 'خرید درون‌برنامه‌ای',        'type': 'checkbox'},
        ]
    },

    'social_media': {
        'label': 'شبکه‌های اجتماعی',
        'icon': '📣',
        'title': 'اطلاعات اختصاصی پیج / کانال',
        'fields': [
            {'name': 'handle',                 'label': 'نام کاربری / Handle',       'type': 'text',  'placeholder': '@username'},
            {'name': 'followers',              'label': 'تعداد فالوور',               'type': 'number'},
            {'name': 'following',              'label': 'تعداد Following',           'type': 'number'},
            {'name': 'posts_count',            'label': 'تعداد پست‌ها',              'type': 'number'},
            {'name': 'engagement_rate',        'label': 'نرخ تعامل (%)',             'type': 'number'},
            {'name': 'avg_reach',              'label': 'میانگین ریچ هر پست',        'type': 'number'},
            {'name': 'avg_story_views',        'label': 'میانگین بازدید استوری',     'type': 'number'},
            {'name': 'post_frequency',         'label': 'تعداد پست در هفته',         'type': 'number'},
            {'name': 'audience_country',       'label': 'کشور اصلی مخاطبان',         'type': 'text',  'placeholder': 'ایران'},
        ]
    },

    'content_media': {
        'label': 'رسانه و محتوا',
        'icon': '🎙️',
        'title': 'اطلاعات اختصاصی رسانه',
        'fields': [
            {'name': 'content_type',           'label': 'نوع محتوا',                 'type': 'text',  'placeholder': 'پادکست / ویدیو / خبرنامه'},
            {'name': 'subscribers',            'label': 'تعداد مشترکین',             'type': 'number'},
            {'name': 'monthly_audience',       'label': 'بینندگان / شنوندگان ماهانه','type': 'number'},
            {'name': 'episodes_count',         'label': 'تعداد قسمت‌های منتشرشده',   'type': 'number'},
            {'name': 'publishing_frequency',   'label': 'دوره انتشار',               'type': 'text',  'placeholder': 'هفتگی / ماهانه'},
            {'name': 'avg_engagement',         'label': 'میانگین تعامل هر قسمت',     'type': 'number'},
            {'name': 'platforms',              'label': 'پلتفرم‌های انتشار',          'type': 'text',  'placeholder': 'اسپاتیفای، کست‌باکس، یوتیوب'},
        ]
    },

    'domain': {
        'label': 'دامنه',
        'icon': '🔗',
        'title': 'اطلاعات اختصاصی دامنه',
        'fields': [
            {'name': 'domain_name',            'label': 'نام دامنه',                     'type': 'text',  'placeholder': 'example.com', 'ltr': True},
            {'name': 'extension',              'label': 'پسوند',                         'type': 'text',  'placeholder': '.com / .ir'},
            {'name': 'domain_age_years',       'label': 'سن دامنه (سال)',                'type': 'number'},
            {'name': 'monthly_type_in',        'label': 'ترافیک تایپ-این ماهانه',        'type': 'number'},
            {'name': 'backlinks_count',        'label': 'تعداد بک‌لینک',                  'type': 'number'},
            {'name': 'keyword',                'label': 'کلمه کلیدی اصلی',               'type': 'text'},
            {'name': 'search_volume',          'label': 'حجم جستجوی ماهانه کلمه',       'type': 'number'},
            {'name': 'is_brandable',           'label': 'برندی / کوتاه است',             'type': 'checkbox'},
        ]
    },

    'service_business': {
        'label': 'کسب‌وکار خدماتی آنلاین',
        'icon': '💼',
        'title': 'اطلاعات اختصاصی کسب‌وکار',
        'fields': [
            {'name': 'services_list',          'label': 'خدمات ارائه‌شده',              'type': 'textarea', 'placeholder': 'سئو، طراحی، مارکتینگ...'},
            {'name': 'team_size',              'label': 'اندازه تیم',                    'type': 'number'},
            {'name': 'active_clients',         'label': 'تعداد مشتریان فعال',            'type': 'number'},
            {'name': 'avg_project_value',      'label': 'میانگین ارزش پروژه (تومان)',   'type': 'number'},
            {'name': 'monthly_projects',       'label': 'تعداد پروژه در ماه',            'type': 'number'},
            {'name': 'client_retention',       'label': 'نرخ حفظ مشتری (%)',             'type': 'number'},
            {'name': 'contracts_count',        'label': 'تعداد قراردادهای فعال',         'type': 'number'},
        ]
    },

    'other': {
        'label': 'سایر',
        'icon': '📦',
        'title': 'اطلاعات تکمیلی',
        'fields': [
            {'name': 'custom_description',     'label': 'توضیحات بیشتر درباره دارایی','type': 'textarea'},
            {'name': 'asset_category',         'label': 'نوع دارایی',                  'type': 'text'},
        ]
    },
}


# ─── نمایش بخش‌های هر مرحله بر اساس دسته اصلی ───
# هر کلید = slug دسته اصلی | مقادیر = True/False برای نمایش هر بخش
STEP_SECTIONS_CONFIG = {
    'website': {
        'step2_income_stats':       True,
        'step2_expenses':           True,
        'step2_monetization':       True,
        'step4_charts':             True,
        'step4_platform_stats':     True,
        'step5_social_media':       True,
        'step5_income_proof':       True,
        'step5_attachments':        True,
        'step5_traffic':            True,
        'step6_technologies':       True,
        'step6_services_used':      True,
    },
    'ecommerce': {
        'step2_income_stats':       True,
        'step2_expenses':           True,
        'step2_monetization':       True,
        'step4_charts':             True,
        'step4_platform_stats':     True,
        'step5_social_media':       True,
        'step5_income_proof':       True,
        'step5_attachments':        True,
        'step5_traffic':            True,
        'step6_technologies':       True,
        'step6_services_used':      True,
    },
    'app': {
        'step2_income_stats':       True,
        'step2_expenses':           True,
        'step2_monetization':       True,
        'step4_charts':             True,
        'step4_platform_stats':     True,
        'step5_social_media':       True,
        'step5_income_proof':       True,
        'step5_attachments':        True,
        'step5_traffic':            True,
        'step6_technologies':       True,
        'step6_services_used':      True,
    },
    'social_media': {
        # چون خودش پیج/کانال است — بخش «رسانه‌های اجتماعی» حذف می‌شود
        'step2_income_stats':       True,
        'step2_expenses':           True,
        'step2_monetization':       True,
        'step4_charts':             True,
        'step4_platform_stats':     False,
        'step5_social_media':       False,   # ← حذف
        'step5_income_proof':       True,
        'step5_attachments':        True,
        'step5_traffic':            True,
        'step6_technologies':       False,
        'step6_services_used':      False,
    },
    'content_media': {
        'step2_income_stats':       True,
        'step2_expenses':           True,
        'step2_monetization':       True,
        'step4_charts':             True,
        'step4_platform_stats':     True,
        'step5_social_media':       True,
        'step5_income_proof':       True,
        'step5_attachments':        True,
        'step5_traffic':            True,
        'step6_technologies':       False,   # رسانه معمولا تکنولوژی نمی‌خواهد
        'step6_services_used':      True,
    },
    'domain': {
        # دامنه ساده‌ترین حالت
        'step2_income_stats':       False,
        'step2_expenses':           False,
        'step2_monetization':       False,
        'step4_charts':             False,
        'step4_platform_stats':     False,
        'step5_social_media':       False,
        'step5_income_proof':       False,
        'step5_attachments':        False,
        'step5_traffic':            False,
        'step6_technologies':       False,
        'step6_services_used':      False,
    },
    'service_business': {
        'step2_income_stats':       True,
        'step2_expenses':           True,
        'step2_monetization':       True,
        'step4_charts':             True,
        'step4_platform_stats':     False,
        'step5_social_media':       True,
        'step5_income_proof':       True,
        'step5_attachments':        True,
        'step5_traffic':            True,
        'step6_technologies':       True,
        'step6_services_used':      True,
    },
    'other': {
        'step2_income_stats':       False,
        'step2_expenses':           False,
        'step2_monetization':       False,
        'step4_charts':             False,
        'step4_platform_stats':     False,
        'step5_social_media':       False,
        'step5_income_proof':       False,
        'step5_attachments':        True,
        'step5_traffic':            False,
        'step6_technologies':       False,
        'step6_services_used':      False,
    },
}

# دسته‌های پلتفرم به تفکیک دسته اصلی — برای پیدا کردن دسته اصلی از sub_slug
def get_main_category(sub_slug: str):
    from .models import Category
    for slug, label, subs in Category.PLATFORM_CATEGORIES:
        for s, _ in subs:
            if s == sub_slug:
                return slug
    return 'other'

def get_sections_for_sub(sub_slug: str):
    main = get_main_category(sub_slug)
    return STEP_SECTIONS_CONFIG.get(main, STEP_SECTIONS_CONFIG['other'])

def get_fields_for_sub(sub_slug: str):
    main = get_main_category(sub_slug)
    cfg = CATEGORY_FORM_CONFIG.get(main, CATEGORY_FORM_CONFIG['other'])
    return cfg