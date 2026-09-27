"""Create realistic, idempotent examples for every listing-card family."""

from datetime import date
from xml.sax.saxutils import escape

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from listings.models import (
    AppDetails,
    ContentMediaDetails,
    DomainDetails,
    EcommerceDetails,
    Expense,
    IncomeDataPoint,
    Listing,
    ListingFAQ,
    MonetizationMethod,
    SaleInclude,
    ServiceBusinessDetails,
    SocialMediaDetails,
    TrafficSource,
    ViewsDataPoint,
    WebsiteDetails,
)


def svg_cover(title, accent):
    """A local SVG cover means seeded visual listings never need a remote image."""
    safe_title = escape(title[:34])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675">
      <defs><linearGradient id="g" x1="0" x2="1" y1="0" y2="1"><stop stop-color="{accent}"/><stop offset="1" stop-color="#111c38"/></linearGradient></defs>
      <rect width="1200" height="675" fill="url(#g)"/><circle cx="1000" cy="130" r="210" fill="#fff" opacity=".08"/>
      <path d="M0 560C230 460 390 710 640 555s330-10 560-120v240H0Z" fill="#fff" opacity=".1"/>
      <text x="74" y="300" fill="#fff" font-family="Arial, sans-serif" font-size="50" font-weight="700">{safe_title}</text>
      <text x="74" y="360" fill="#fff" opacity=".75" font-family="Arial, sans-serif" font-size="25">Digital asset marketplace</text>
    </svg>'''


class Command(BaseCommand):
    help = "ایجاد دو آگهی نمایشی حرفه‌ای برای هر نوع کارت آگهی"

    def handle(self, *args, **options):
        user_model = get_user_model()
        seller, _ = user_model.objects.get_or_create(
            username="demo_listing_seller",
            defaults={"email": "demo-listings@example.test"},
        )
        if not seller.has_usable_password():
            seller.set_unusable_password()
            seller.save(update_fields=["password"])

        samples = [
            ("website", "website_blog", "مجله تخصصی خانه هوشمند با رشد ارگانیک", "#3157d5", {
                "price": 1_850_000_000, "discount_price": 1_690_000_000, "monthly_income": 78_000_000,
                "avg_monthly_profit": 58_000_000, "profit_margin": 74, "platform_age": 54,
                "areas_activity": "tech_apps", "views_count": 32_400, "followers_count": 18_600,
                "platform_url": "https://smart-home.example.test",
                "description": "رسانه محتوایی فارسی در حوزه خانه هوشمند با ترافیک ارگانیک پایدار، آرشیو عمیق و همکاری‌های تجاری فعال. انتقال دامنه، محتوای تولیدشده و فرآیندهای انتشار مستند انجام می‌شود.",
                "details": {"monthly_visits": 186000, "unique_visitors": 132000, "page_views": 268000, "content_count": 1240, "domain_authority": 37, "backlinks_count": 8400, "bounce_rate": 41.2},
            }),
            ("website", "website_educational", "پلتفرم آموزش زبان با فروش دوره ضبط‌شده", "#0f766e", {
                "price": 2_400_000_000, "monthly_income": 112_000_000, "avg_monthly_profit": 81_000_000,
                "profit_margin": 72, "platform_age": 38, "areas_activity": "education_languages", "views_count": 21_700,
                "followers_count": 9400, "platform_url": "https://lingo-course.example.test",
                "description": "پلتفرم آموزش زبان با ۲۸ دوره و قیف فروش خودکار. درآمد از فروش دوره، عضویت ویژه و کلاس‌های تکمیلی ایجاد می‌شود و محتوای آموزشی آماده انتقال است.",
                "details": {"monthly_visits": 92000, "unique_visitors": 64000, "page_views": 177000, "content_count": 610, "domain_authority": 29, "backlinks_count": 3100},
            }),
            ("ecommerce", "ecommerce_woocommerce", "فروشگاه تخصصی تجهیزات سفر و کمپینگ", "#c05621", {
                "price": 3_200_000_000, "monthly_income": 245_000_000, "avg_monthly_profit": 69_000_000,
                "profit_margin": 28, "platform_age": 47, "areas_activity": "sports_camping", "views_count": 48_500,
                "platform_url": "https://camp-shop.example.test", "description": "فروشگاه ووکامرسی با مشتریان بازگشتی، قرارداد تأمین‌کننده و فرآیند ارسال استاندارد. موجودی قابل انتقال و تیم عملیاتی دو نفره در مجموعه باقی می‌مانند.",
                "details": {"products_count": 860, "orders_per_month": 1250, "aov": 196000, "conversion_rate": 2.8, "returning_customers": 34, "has_inventory": True, "inventory_value": 920000000, "shipping_partners": "پست، تیپاکس، چاپار"},
            }),
            ("ecommerce", "ecommerce_marketplace_shop", "فروشگاه لوازم جانبی موبایل در مارکت‌پلیس", "#7c3aed", {
                "price": 1_150_000_000, "monthly_income": 96_000_000, "avg_monthly_profit": 31_000_000,
                "profit_margin": 32, "platform_age": 31, "areas_activity": "electronics_mobile", "views_count": 18_900,
                "platform_url": "https://market-shop.example.test", "description": "ویترین فعال لوازم جانبی موبایل با امتیاز فروشنده ممتاز، تأمین‌کنندگان ثابت و محصولات پرفروش مشخص. موجودی و اکانت فروشنده طبق قرارداد منتقل می‌شود.",
                "details": {"products_count": 410, "orders_per_month": 740, "aov": 310000, "conversion_rate": 4.1, "returning_customers": 22, "has_inventory": True, "inventory_value": 480000000},
            }),
            ("app", "app_saas", "SaaS مدیریت نوبت و پرونده کلینیک", "#2563eb", {
                "price": 4_800_000_000, "monthly_income": 320_000_000, "avg_monthly_profit": 205_000_000,
                "profit_margin": 64, "platform_age": 42, "areas_activity": "tech_saas", "views_count": 14_800,
                "platform_url": "https://clinic-flow.example.test", "description": "نرم‌افزار SaaS مدیریت نوبت، پرونده و پیامک یادآوری با قراردادهای سالانه کلینیک‌ها. سورس، زیرساخت و مستندات استقرار در معامله قرار دارد.",
                "details": {"downloads": 0, "active_installs": 0, "mau": 5600, "dau": 2100, "rating": 4.8, "reviews_count": 183, "retention_rate": 91, "current_version": "3.8.2", "has_in_app_purchase": False},
            }),
            ("app", "app_android", "اپلیکیشن برنامه‌ریزی مطالعه کنکور", "#db2777", {
                "price": 2_100_000_000, "monthly_income": 145_000_000, "avg_monthly_profit": 96_000_000,
                "profit_margin": 66, "platform_age": 28, "areas_activity": "education_colleges_courses", "views_count": 39_200,
                "platform_url": "https://study-plan.example.test", "description": "اپلیکیشن اندرویدی برنامه‌ریزی مطالعه با اشتراک ماهانه، جامعه فعال دانش‌آموزان و محتوای قابل به‌روزرسانی. اکانت استور و پنل مدیریت با انتقال کامل واگذار می‌شود.",
                "details": {"downloads": 184000, "active_installs": 68200, "mau": 22100, "dau": 6800, "rating": 4.6, "reviews_count": 2460, "retention_rate": 49, "current_version": "2.7.0", "has_in_app_purchase": True},
            }),
            ("social_media", "social_instagram", "پیج اینستاگرام طراحی داخلی مینیمال", "#be185d", {
                "price": 980_000_000, "monthly_income": 52_000_000, "avg_monthly_profit": 44_000_000,
                "profit_margin": 85, "platform_age": 51, "areas_activity": "design_style", "views_count": 81_000,
                "followers_count": 284000, "platform_url": "https://instagram.com/interior.example", "description": "پیج طراحی داخلی با جامعه مخاطب واقعی، نرخ تعامل پایدار و همکاری‌های تبلیغاتی مستمر. آرشیو محتوا، تقویم انتشار و ارتباط با برندها تحویل داده می‌شود.",
                "details": {"handle": "@interior.example", "followers": 284000, "posts_count": 1280, "engagement_rate": 4.7, "avg_reach": 68500, "audience_country": "ایران", "audience_age_range": "۲۵ تا ۳۴", "is_monetized": True},
            }),
            ("social_media", "social_telegram_channel", "کانال تلگرام تحلیل بازار فناوری", "#0891b2", {
                "price": 760_000_000, "monthly_income": 36_000_000, "avg_monthly_profit": 30_000_000,
                "profit_margin": 83, "platform_age": 63, "areas_activity": "tech_ai", "views_count": 57_000,
                "followers_count": 96000, "platform_url": "https://t.me/techbrief_example", "description": "کانال خبری و تحلیلی فناوری با مخاطبان علاقه‌مند به استارتاپ و هوش مصنوعی. مدل درآمدی از رپورتاژ تخصصی و اسپانسرهای ماهانه تشکیل شده است.",
                "details": {"handle": "@techbrief_example", "followers": 96000, "posts_count": 4760, "engagement_rate": 18.4, "avg_reach": 17600, "audience_country": "ایران", "audience_age_range": "۲۴ تا ۴۰", "is_monetized": True},
            }),
            ("content_media", "content_podcast", "پادکست روایت کسب‌وکار با اسپانسر ثابت", "#9333ea", {
                "price": 1_450_000_000, "monthly_income": 88_000_000, "avg_monthly_profit": 62_000_000,
                "profit_margin": 70, "platform_age": 44, "areas_activity": "business_productivity", "views_count": 26_300,
                "platform_url": "https://podcast-business.example.test", "description": "پادکست هفتگی مصاحبه با بنیان‌گذاران کسب‌وکار، دارای آرشیو ۱۴۰ قسمت و قراردادهای اسپانسری قابل تمدید. تجهیزات ضبط و فرمت تولید مستند شده‌اند.",
                "details": {"content_type": "podcast", "subscribers": 48600, "monthly_audience": 132000, "episodes_count": 142, "publishing_frequency": "هفتگی", "avg_engagement": 7800, "platforms": "Castbox، Spotify، شنوتو", "avg_downloads": 11200},
            }),
            ("content_media", "content_newsletter", "خبرنامه تخصصی اقتصاد دیجیتال", "#ca8a04", {
                "price": 620_000_000, "monthly_income": 31_000_000, "avg_monthly_profit": 25_000_000,
                "profit_margin": 81, "platform_age": 26, "areas_activity": "business_finance", "views_count": 12_600,
                "platform_url": "https://newsletter-digital.example.test", "description": "خبرنامه ایمیلی سه‌بار در هفته با جامعه مدیران و فعالان اقتصاد دیجیتال. فهرست مشترکان رضایتمند، قالب‌های آماده و تقویم محتوایی انتقال داده می‌شود.",
                "details": {"content_type": "newsletter", "subscribers": 21800, "monthly_audience": 56400, "episodes_count": 312, "publishing_frequency": "سه بار در هفته", "avg_engagement": 8100, "platforms": "Brevo، وب‌سایت", "open_rate": 42.5, "click_rate": 8.3},
            }),
            ("domain", "domain_com", "دامنه کوتاه و برندپذیر Novexa.com", "#1d4ed8", {
                "price": 420_000_000, "platform_age": 0, "areas_activity": "internet_domaining", "views_count": 3200,
                "description": "دامنه کوتاه، خوش‌خوان و مناسب محصول فناوری یا برند بین‌المللی. مالکیت در رجیسترار معتبر منتقل و فرایند انتقال پس از تسویه کامل شروع می‌شود.",
                "details": {"domain_name": "novexa.com", "registrar": "Namecheap", "expiry_date": date(2028, 11, 16), "domain_age_years": 9.4, "monthly_type_in": 380, "backlinks_count": 42, "keyword": "novexa", "search_volume": 260},
            }),
            ("domain", "domain_ir", "دامنه فارسی و تجاری خانه‌سبز.ir", "#15803d", {
                "price": 185_000_000, "platform_age": 0, "areas_activity": "home_gardening", "views_count": 2100,
                "description": "دامنه فارسی ساده و به‌یادماندنی برای کسب‌وکارهای حوزه گیاه، دکور و سبک زندگی. انتقال شناسه و دامنه از مسیر رسمی ایرنیک با حضور طرفین انجام می‌شود.",
                "details": {"domain_name": "khanehsabz.ir", "registrar": "ایرنیک", "expiry_date": date(2027, 8, 5), "domain_age_years": 6.1, "monthly_type_in": 190, "backlinks_count": 18, "keyword": "خانه سبز", "search_volume": 1900},
            }),
            ("service_business", "service_agency", "آژانس رشد دیجیتال با قراردادهای اشتراکی", "#0f766e", {
                "price": 5_600_000_000, "monthly_income": 410_000_000, "avg_monthly_profit": 168_000_000,
                "profit_margin": 41, "platform_age": 72, "areas_activity": "business_sales_marketing", "views_count": 9800,
                "platform_url": "https://growth-agency.example.test", "description": "آژانس دیجیتال مارکتینگ با قراردادهای ماهانه، تیم ثابت و فرآیندهای عملیاتی قابل انتقال. مشتریان کلیدی و ابزارهای مدیریت پروژه طبق برنامه تحویل واگذار می‌شوند.",
                "details": {"services_list": "SEO، تبلیغات کلیکی، طراحی لندینگ و اتوماسیون بازاریابی", "team_size": 9, "active_clients": 34, "total_clients": 186, "avg_project_value": 48000000, "monthly_projects": 11, "client_retention": 78, "recurring_revenue_pct": 74, "contracts_count": 29},
            }),
            ("service_business", "service_booking", "سامانه رزرو آنلاین سالن‌های زیبایی", "#e11d48", {
                "price": 2_950_000_000, "monthly_income": 186_000_000, "avg_monthly_profit": 104_000_000,
                "profit_margin": 56, "platform_age": 35, "areas_activity": "health_beauty_general", "views_count": 17_600,
                "platform_url": "https://beauty-booking.example.test", "description": "کسب‌وکار خدماتی رزرو آنلاین با پنل سالن‌ها، پیامک یادآوری و درآمد کارمزدی. قراردادهای فعال و تیم پشتیبانی برای دوره انتقال در دسترس خواهند بود.",
                "details": {"services_list": "رزرو آنلاین، پنل سالن، پیامک یادآوری و پرداخت", "team_size": 5, "active_clients": 128, "total_clients": 386, "avg_project_value": 1450000, "monthly_projects": 4200, "client_retention": 84, "recurring_revenue_pct": 88},
            }),
            ("other", "other_misc", "کتابخانه قالب‌های حرفه‌ای ارائه و فروش", "#475569", {
                "price": 340_000_000, "platform_age": 18, "areas_activity": "design_logos", "views_count": 5200,
                "platform_url": "https://presentation-assets.example.test", "description": "مجموعه‌ای از قالب‌های حرفه‌ای فارسی برای ارائه و شبکه‌های اجتماعی، همراه با فایل‌های منبع و راهنمای تولید. حقوق فروش و نام تجاری مرتبط انتقال داده می‌شود.",
                "details": {"asset_category": "مجموعه فایل دیجیتال", "custom_description": "بیش از ۴۵۰ قالب قابل ویرایش در PowerPoint، Figma و Canva همراه با مجوز بازفروش."},
            }),
            ("other", "other_misc", "بانک نام و هویت بصری برندهای آماده", "#334155", {
                "price": 510_000_000, "platform_age": 24, "areas_activity": "design_logos", "views_count": 7100,
                "description": "آرشیو نام‌های برند، لوگوهای اولیه و دامنه‌های پیشنهادی برای استارتاپ‌ها. ساختار دسته‌بندی و فایل‌های منبع برای واگذاری کامل آماده شده‌اند.",
                "details": {"asset_category": "آرشیو هویت بصری", "custom_description": "۱۲۰ نام برند پژوهش‌شده با لوگوی اولیه، رنگ‌بندی و بررسی اولیه امکان ثبت دامنه."},
            }),
        ]

        detail_models = {
            "website": WebsiteDetails, "ecommerce": EcommerceDetails, "app": AppDetails,
            "social_media": SocialMediaDetails, "content_media": ContentMediaDetails,
            "domain": DomainDetails, "service_business": ServiceBusinessDetails,
        }
        created_count = 0
        for family, category, title, accent, data in samples:
            details = data.pop("details")
            serializable_details = {
                key: value.isoformat() if isinstance(value, date) else value
                for key, value in details.items()
            }
            defaults = {
                **data, "seller": seller, "category": category, "title": title,
                "status": "active", "is_income": family not in {"domain", "other"},
                "is_verified": True, "suggested_price": True, "is_private": title.startswith("SaaS"),
                "asset_details": serializable_details, "sale_type": "full_ownership",
                "about_platform": "<p>نمونه‌داده نمایشی برای بررسی ساختار کارت و صفحه جزئیات آگهی.</p>",
            }
            listing, created = Listing.objects.update_or_create(seller=seller, title=title, defaults=defaults)
            created_count += int(created)
            if family not in {"domain", "other"} and not listing.main_image:
                listing.main_image.save(f"demo-{listing.pk}.svg", ContentFile(svg_cover(title, accent)), save=True)

            detail_model = detail_models.get(family)
            if detail_model:
                detail_model.objects.update_or_create(listing=listing, defaults=details)
            SaleInclude.objects.get_or_create(listing=listing, asset_name="دسترسی‌ها و مستندات انتقال")
            ListingFAQ.objects.get_or_create(listing=listing, question="فرایند انتقال چگونه است?", defaults={"answer": "پس از توافق و تسویه، دسترسی‌ها طبق چک‌لیست تحویل داده می‌شوند.", "order": 1})
            if family not in {"domain", "other"}:
                Expense.objects.get_or_create(listing=listing, expense_name="هزینه زیرساخت و عملیات", defaults={"amount": max(int(data.get("monthly_income", 0) * 0.12), 1000000), "period": "monthly"})
                MonetizationMethod.objects.get_or_create(listing=listing, method="providing_consulting_services" if family == "service_business" else "special_subscription_sale")
                for month, income, views in ((date(2026, 4, 1), 0.92, 0.88), (date(2026, 5, 1), 0.98, 0.96), (date(2026, 6, 1), 1, 1.08)):
                    IncomeDataPoint.objects.update_or_create(listing=listing, date=month, defaults={"income": int(data["monthly_income"] * income)})
                    ViewsDataPoint.objects.update_or_create(listing=listing, date=month, defaults={"views": int(data["views_count"] * views)})
                TrafficSource.objects.update_or_create(listing=listing, source="organic_search", defaults={"percentage": 58})
                TrafficSource.objects.update_or_create(listing=listing, source="direct", defaults={"percentage": 27})
                TrafficSource.objects.update_or_create(listing=listing, source="social_media", defaults={"percentage": 15})

        self.stdout.write(self.style.SUCCESS(f"{len(samples)} آگهی نمونه آماده است ({created_count} مورد جدید)."))
