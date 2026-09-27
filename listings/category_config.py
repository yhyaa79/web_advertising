"""Central, editable schema for the category-aware listing wizard.

Edit ``BASE_FIELDS`` for a whole asset family and ``SUBCATEGORY_FIELDS`` for
one exact category. The UI and server validation both consume this file.
"""
from copy import deepcopy


def field(name, label, kind="text", *, required=False, placeholder="", help_text="",
          min_value=None, max_value=None, step=None, options=None, ltr=False):
    if not help_text:
        help_text = (
            "این مقدار برای مقایسه دقیق‌تر آگهی‌ها استفاده می‌شود."
            if required else "اختیاری؛ فقط در صورت دسترسی به اطلاعات دقیق وارد کنید."
        )
    item = {"name": name, "label": label, "type": kind, "required": required}
    optional = {"placeholder": placeholder, "help": help_text, "min": min_value,
                "max": max_value, "step": step, "options": options}
    item.update({key: value for key, value in optional.items() if value not in (None, "", [])})
    if ltr:
        item["ltr"] = True
    return item


PERCENT = {"min_value": 0, "max_value": 100, "step": "0.01"}

BASE_FIELDS = {
    "website": [
        field("monthly_visits", "بازدید ماهانه", "number", min_value=0, help_text="میانگین بازدید یک ماه معمولی را وارد کنید."),
        field("unique_visitors", "کاربران یکتای ماهانه", "number", min_value=0),
        field("page_views", "بازدید صفحات ماهانه", "number", min_value=0),
        field("content_count", "تعداد صفحات یا محتواها", "number", min_value=0),
        field("domain_authority", "اعتبار دامنه (DA)", "number", min_value=0, max_value=100),
        field("backlinks_count", "تعداد بک‌لینک", "number", min_value=0),
        field("bounce_rate", "نرخ پرش (درصد)", "number", **PERCENT),
    ],
    "ecommerce": [
        field("products_count", "تعداد محصولات فعال", "number", required=True, min_value=0),
        field("orders_per_month", "میانگین سفارش ماهانه", "number", required=True, min_value=0),
        field("aov", "میانگین ارزش سفارش (تومان)", "number", min_value=0),
        field("conversion_rate", "نرخ تبدیل (درصد)", "number", **PERCENT),
        field("returning_customers", "مشتریان بازگشتی (درصد)", "number", **PERCENT),
        field("has_inventory", "موجودی فیزیکی منتقل می‌شود", "checkbox"),
        field("inventory_value", "ارزش موجودی قابل انتقال (تومان)", "number", min_value=0),
        field("shipping_partners", "روش‌ها یا شرکای ارسال", placeholder="پست، تیپاکس و ..."),
    ],
    "app": [
        field("downloads", "تعداد کل دانلود", "number", min_value=0),
        field("active_installs", "نصب فعال", "number", min_value=0),
        field("mau", "کاربران فعال ماهانه (MAU)", "number", required=True, min_value=0),
        field("dau", "کاربران فعال روزانه (DAU)", "number", min_value=0),
        field("rating", "امتیاز کاربران (از ۵)", "number", min_value=0, max_value=5, step="0.01"),
        field("reviews_count", "تعداد نظرها", "number", min_value=0),
        field("retention_rate", "نرخ نگهداشت (درصد)", "number", **PERCENT),
        field("current_version", "نسخه فعلی", placeholder="مثال: 2.4.1", ltr=True),
        field("last_update_date", "تاریخ آخرین به‌روزرسانی", "date"),
        field("has_in_app_purchase", "خرید درون‌برنامه‌ای فعال است", "checkbox"),
    ],
    "social_media": [
        field("handle", "نام کاربری / شناسه", required=True, placeholder="@username", ltr=True),
        field("followers", "دنبال‌کننده یا عضو", "number", required=True, min_value=0),
        field("posts_count", "تعداد محتوای منتشرشده", "number", min_value=0),
        field("engagement_rate", "نرخ تعامل (درصد)", "number", **PERCENT),
        field("avg_reach", "میانگین دسترسی هر محتوا", "number", min_value=0),
        field("audience_country", "کشور اصلی مخاطبان", placeholder="ایران"),
        field("audience_age_range", "بازه سنی غالب مخاطبان", placeholder="مثال: ۱۸ تا ۲۴"),
        field("is_monetized", "قابلیت درآمدزایی فعال است", "checkbox"),
        field("has_verification", "حساب تأییدشده است", "checkbox"),
    ],
    "content_media": [
        field("subscribers", "تعداد مشترکان", "number", required=True, min_value=0),
        field("monthly_audience", "مخاطب ماهانه", "number", required=True, min_value=0),
        field("episodes_count", "تعداد محتواهای منتشرشده", "number", min_value=0),
        field("publishing_frequency", "برنامه انتشار", placeholder="مثال: هفتگی"),
        field("avg_engagement", "میانگین تعامل هر محتوا", "number", min_value=0),
        field("platforms", "پلتفرم‌های انتشار", placeholder="یوتیوب، کست‌باکس و ..."),
        field("avg_downloads", "میانگین دانلود / پخش", "number", min_value=0),
    ],
    "domain": [
        field("domain_name", "نام دامنه", required=True, placeholder="example.com", ltr=True),
        field("registrar", "ثبت‌کننده دامنه", required=True, placeholder="ایرنیک، Namecheap و ..."),
        field("expiry_date", "تاریخ انقضا", "date", required=True),
        field("domain_age_years", "سن دامنه (سال)", "number", min_value=0, step="0.1"),
        field("monthly_type_in", "ورودی مستقیم ماهانه", "number", min_value=0),
        field("backlinks_count", "تعداد بک‌لینک", "number", min_value=0),
        field("keyword", "کلیدواژه اصلی"), field("search_volume", "جست‌وجوی ماهانه کلیدواژه", "number", min_value=0),
        field("has_history", "دامنه سابقه وب‌سایت دارد", "checkbox"),
    ],
    "service_business": [
        field("services_list", "خدمات اصلی", "textarea", required=True),
        field("team_size", "تعداد اعضای تیم", "number", required=True, min_value=1),
        field("active_clients", "مشتریان فعال", "number", required=True, min_value=0),
        field("total_clients", "کل مشتریان تا امروز", "number", min_value=0),
        field("avg_project_value", "میانگین ارزش پروژه (تومان)", "number", min_value=0),
        field("monthly_projects", "پروژه‌های جدید در ماه", "number", min_value=0),
        field("client_retention", "نرخ حفظ مشتری (درصد)", "number", **PERCENT),
        field("recurring_revenue_pct", "درآمد تکرارشونده (درصد)", "number", **PERCENT),
    ],
    "other": [field("asset_category", "نوع دقیق دارایی", required=True),
              field("custom_description", "مشخصات تخصصی دارایی", "textarea", required=True)],
}


# All selectable subcategories are deliberately explicit. Add/edit questions here.
SUBCATEGORY_FIELDS = {
    "website_blog": [field("publishing_frequency", "تعداد محتوای جدید در ماه", "number", min_value=0)],
    "website_news_magazine": [field("daily_articles", "میانگین خبر / مقاله روزانه", "number", min_value=0)],
    "website_forum_community": [field("registered_members", "اعضای ثبت‌نام‌شده", "number", min_value=0), field("monthly_posts", "پست ماهانه انجمن", "number", min_value=0)],
    "website_educational": [field("students_count", "دانشجویان ثبت‌نام‌شده", "number", min_value=0), field("courses_count", "تعداد دوره‌ها", "number", min_value=0)],
    "website_job_board": [field("active_jobs", "فرصت‌های شغلی فعال", "number", min_value=0), field("employers_count", "کارفرمایان عضو", "number", min_value=0)],
    "website_real_estate": [field("active_property_ads", "آگهی ملک فعال", "number", min_value=0)],
    "website_other": [field("website_model", "مدل و کارکرد وب‌سایت")],
    "ecommerce_woocommerce": [field("plugin_count", "افزونه‌های کلیدی فعال", "number", min_value=0)],
    "ecommerce_shopify": [field("shopify_plan", "پلن فعلی Shopify")],
    "ecommerce_custom": [field("source_code_transfer", "سورس‌کد کامل منتقل می‌شود", "checkbox")],
    "ecommerce_marketplace_shop": [field("marketplace_name", "نام مارکت‌پلیس", required=True), field("seller_score", "امتیاز فروشنده")],
    "ecommerce_dropship": [field("supplier_agreements", "توافق فعال با تأمین‌کنندگان", "checkbox")],
    "ecommerce_woo_fba_dropship": [field("fulfillment_model", "مدل تامین و ارسال", required=True)],
    "ecommerce_other": [field("commerce_model", "مدل فروش")],
    "app_android": [field("store_url", "لینک Google Play / کافه‌بازار", "url", ltr=True)],
    "app_ios": [field("store_url", "لینک App Store", "url", ltr=True)],
    "app_cross_platform": [field("framework", "فریم‌ورک", "select", options=[["flutter", "Flutter"], ["react_native", "React Native"], ["other", "سایر"]])],
    "app_game_mobile": [field("monthly_players", "بازیکن ماهانه", "number", min_value=0)],
    "app_saas": [field("paying_customers", "مشتریان پرداخت‌کننده", "number", required=True, min_value=0), field("churn_rate", "نرخ ریزش ماهانه (درصد)", "number", **PERCENT)],
    "app_telegram_bot": [field("bot_users", "کاربران فعال ربات", "number", required=True, min_value=0)],
    "app_web_tool": [field("delivery_platform", "بستر ارائه", placeholder="وب‌اپ، افزونه یا API")],
    "app_other": [field("delivery_platform", "بستر ارائه")],
    "social_instagram": [field("avg_story_views", "میانگین بازدید استوری", "number", min_value=0)],
    "social_telegram_channel": [field("avg_post_views", "میانگین بازدید هر پست", "number", min_value=0)],
    "social_telegram_group": [field("daily_messages", "میانگین پیام روزانه", "number", min_value=0)],
    "social_youtube": [field("watch_hours_28d", "ساعت تماشا در ۲۸ روز", "number", min_value=0)],
    "social_aparat": [field("monthly_video_views", "بازدید ویدیو ماهانه", "number", min_value=0)],
    "social_twitter_x": [field("monthly_impressions", "ایمپرشن ماهانه", "number", min_value=0)],
    "social_linkedin": [field("page_type", "نوع صفحه", "select", options=[["company", "شرکتی"], ["personal", "شخصی"]])],
    "social_tiktok": [field("avg_video_views", "میانگین بازدید ویدیو", "number", min_value=0)],
    "social_other": [field("network_name", "نام شبکه اجتماعی", required=True)],
    "content_podcast": [field("avg_episode_downloads", "میانگین دانلود هر قسمت", "number", min_value=0)],
    "content_newsletter": [field("open_rate", "نرخ بازشدن ایمیل (درصد)", "number", **PERCENT), field("click_rate", "نرخ کلیک (درصد)", "number", **PERCENT)],
    "content_adsense_channel": [field("monthly_ad_impressions", "نمایش تبلیغ ماهانه", "number", min_value=0)],
    "content_ebook_course": [field("units_sold", "تعداد فروش تا امروز", "number", min_value=0)],
    "domain_com": [], "domain_ir": [],
    "domain_international_other": [field("extension", "پسوند دامنه", required=True)],
    "domain_brandable": [field("is_brandable", "نام دامنه کوتاه و برندپذیر است", "checkbox")],
    "domain_portfolio": [field("portfolio_size", "تعداد دامنه‌های مجموعه", "number", required=True, min_value=2)],
    "service_agency": [field("contracts_count", "قرارداد فعال", "number", min_value=0)],
    "service_consulting": [field("consulting_hours_monthly", "ساعت مشاوره ماهانه", "number", min_value=0)],
    "service_membership_site": [field("paid_members", "اعضای پرداخت‌کننده", "number", min_value=0)],
    "service_marketplace": [field("monthly_transactions", "تراکنش ماهانه", "number", min_value=0)],
    "service_booking": [field("monthly_bookings", "رزرو ماهانه", "number", min_value=0)],
    "service_sms_marketing": [field("monthly_sends", "میانگین ارسال ماهانه", "number", min_value=0)],
    "service_other": [field("service_model", "مدل ارائه خدمت", required=True)],
    "other_misc": [],
}

# Some legacy subcategory slugs live under a different menu heading.  The
# prefix determines the asset family, and therefore its form, data model and
# list card, rather than the menu section where it happens to be displayed.
MAIN_CATEGORY_OVERRIDES = {
    "software": "app",
    "website_blog": "website",
    "website_news_magazine": "website",
    "website_forum_community": "website",
    "website_educational": "website",
    "website_job_board": "website",
    "website_real_estate": "website",
    "website_other": "website",
}

CATEGORY_META = {
    # Flags below control entire wizard stages/sections. They are intentionally
    # kept here so category behaviour can be changed without editing HTML/JS.
    "website": {"label": "وب‌سایت", "icon": "website", "financial": True, "charts": True, "traffic": True, "monetization": True, "technical": True, "social_links": True, "licenses": True, "services": True, "income_proof": True, "requires_main_image": True},
    "ecommerce": {"label": "فروشگاه اینترنتی", "icon": "ecommerce", "financial": True, "charts": True, "traffic": True, "monetization": True, "technical": True, "social_links": True, "licenses": True, "services": True, "income_proof": True, "requires_main_image": True},
    "app": {"label": "اپلیکیشن", "icon": "app", "financial": True, "charts": True, "traffic": True, "monetization": True, "technical": True, "social_links": True, "licenses": True, "services": True, "income_proof": True, "requires_main_image": True},
    "social_media": {"label": "شبکه اجتماعی", "icon": "social", "financial": True, "charts": True, "traffic": False, "monetization": True, "technical": False, "social_links": False, "licenses": False, "services": False, "income_proof": True, "requires_main_image": True},
    "content_media": {"label": "رسانه و محتوا", "icon": "media", "financial": True, "charts": True, "traffic": True, "monetization": True, "technical": False, "social_links": True, "licenses": True, "services": True, "income_proof": True, "requires_main_image": True},
    "domain": {"label": "دامنه", "icon": "domain", "financial": False, "charts": False, "traffic": False, "monetization": False, "technical": False, "social_links": False, "licenses": False, "services": False, "income_proof": False, "requires_main_image": False},
    "service_business": {"label": "کسب‌وکار خدماتی", "icon": "service", "financial": True, "charts": True, "traffic": False, "monetization": True, "technical": False, "social_links": True, "licenses": True, "services": True, "income_proof": True, "requires_main_image": True},
    "other": {"label": "سایر", "icon": "other", "financial": False, "charts": False, "traffic": False, "monetization": False, "technical": False, "social_links": False, "licenses": False, "services": False, "income_proof": False, "requires_main_image": False},
}

# ── کارت لیست آگهی: فیلدهایی که برای بینندهٔ بدون دسترسی (آگهی خصوصی) ماسک می‌شوند ──
# کلیدها همان slug دستهٔ اصلی (website, domain, …) هستند — برای تغییر رفتار فقط اینجا را ویرایش کنید.
LISTING_CARD_PRIVATE_FIELDS = {
    "website": ["price", "discount_price", "monthly_income", "profit_margin", "roi", "platform_url", "description", "monthly_visits"],
    "ecommerce": ["price", "discount_price", "monthly_income", "profit_margin", "roi", "platform_url", "description", "orders_per_month"],
    "app": ["price", "discount_price", "monthly_income", "profit_margin", "roi", "platform_url", "description", "mau"],
    "social_media": ["price", "discount_price", "monthly_income", "profit_margin", "roi", "platform_url", "description", "followers", "engagement_rate"],
    "content_media": ["price", "discount_price", "monthly_income", "profit_margin", "roi", "platform_url", "description", "subscribers"],
    "domain": ["price", "discount_price", "monthly_income", "platform_url", "description", "domain_name", "keyword", "search_volume", "expiry_date"],
    "service_business": ["price", "discount_price", "monthly_income", "profit_margin", "roi", "platform_url", "description", "active_clients"],
    "other": ["price", "discount_price", "monthly_income", "platform_url", "description"],
}

# image = ماسک روی تصویر کارت (علاوه بر فیلدهای بالا)
LISTING_CARD_PRIVATE_IMAGE = {
    "website": True,
    "ecommerce": True,
    "app": True,
    "social_media": True,
    "content_media": True,
    "domain": False,
    "service_business": True,
    "other": True,
}

LISTING_CARD_SHOW_IMAGE = {
    "domain": False,
}


def get_main_category(sub_slug):
    if sub_slug in CATEGORY_META:
        return sub_slug
    if sub_slug in MAIN_CATEGORY_OVERRIDES:
        return MAIN_CATEGORY_OVERRIDES[sub_slug]
    if sub_slug.startswith("app_"):
        return "app"
    from .models import Category
    for main_slug, _label, subs in Category.PLATFORM_CATEGORIES:
        if any(slug == sub_slug for slug, _ in subs):
            return main_slug
    return "other"


def get_fields_for_sub(sub_slug):
    main = get_main_category(sub_slug)
    fields = deepcopy(BASE_FIELDS.get(main, BASE_FIELDS["other"])) + deepcopy(SUBCATEGORY_FIELDS.get(sub_slug, []))
    unique = {item["name"]: item for item in fields}  # subtype refines; never asks twice
    result = deepcopy(CATEGORY_META.get(main, CATEGORY_META["other"]))
    meta = CATEGORY_META.get(main, CATEGORY_META["other"])
    result.update({
        "main": main,
        "subcategory": sub_slug,
        "fields": list(unique.values()),
        "requires_main_image": meta.get("requires_main_image", True),
    })
    return result


def category_requires_main_image(sub_slug):
    main = get_main_category(sub_slug)
    return CATEGORY_META.get(main, CATEGORY_META["other"]).get("requires_main_image", True)


def get_listing_card_private_fields(main_slug):
    return LISTING_CARD_PRIVATE_FIELDS.get(main_slug, LISTING_CARD_PRIVATE_FIELDS["other"])


def listing_card_masks_image(main_slug):
    return LISTING_CARD_PRIVATE_IMAGE.get(main_slug, True)


def listing_card_show_image(main_slug):
    return LISTING_CARD_SHOW_IMAGE.get(main_slug, True)


def build_category_form_config():
    from .models import Category
    result = {}
    for _main, _label, subs in Category.PLATFORM_CATEGORIES:
        for sub_slug, sub_label in subs:
            config = get_fields_for_sub(sub_slug)
            config.update({"label": sub_label, "title": f"مشخصات {sub_label}"})
            result[sub_slug] = config
    return result


def validate_category_config():
    from .models import Category
    selectable = {slug for slug, _ in Category.PLATFORM_CHOICES}
    errors = []
    missing, extra = selectable - set(SUBCATEGORY_FIELDS), set(SUBCATEGORY_FIELDS) - selectable
    if missing:
        errors.append("Missing subcategory configuration: " + ", ".join(sorted(missing)))
    if extra:
        errors.append("Unknown subcategory configuration: " + ", ".join(sorted(extra)))
    for slug, config in build_category_form_config().items():
        names = [item["name"] for item in config["fields"]]
        if len(names) != len(set(names)):
            errors.append(f"Duplicate field names for {slug}")
    return errors


# Compatibility for existing detail pages/imports.
CATEGORY_FORM_CONFIG = CATEGORY_META
STEP_SECTIONS_CONFIG = {
    key: {"step2_income_stats": meta["financial"], "step2_expenses": meta["financial"],
          "step2_monetization": meta["financial"], "step4_charts": meta["financial"],
          "step4_platform_stats": meta["traffic"], "step5_social_media": key not in {"social_media", "domain", "other"},
          "step5_income_proof": meta["financial"], "step5_attachments": True,
          "step5_traffic": meta["traffic"], "step6_technologies": meta["technical"],
          "step6_services_used": meta["technical"]}
    for key, meta in CATEGORY_META.items()
}


def get_sections_for_sub(sub_slug):
    return STEP_SECTIONS_CONFIG.get(get_main_category(sub_slug), STEP_SECTIONS_CONFIG["other"])
