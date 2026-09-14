import base64
import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .category_config import build_category_form_config, validate_category_config
from .content_sanitizer import build_safe_rich_content
from .models import (
    Attachment, Category, DomainDetails, Expense, IncomeDataPoint, IncomeProof,
    License, Listing, ListingFAQ, MonetizationMethod, SaleInclude, ServiceUsed,
    SocialMedia, TechnologyUsed, TrafficSource, ViewsDataPoint, WebsiteDetails,
)


TEST_MEDIA_ROOT = tempfile.mkdtemp(prefix="listing-tests-")


def image_file(name="cover.png"):
    content = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
    )
    return SimpleUploadedFile(name, content, content_type="image/png")


@override_settings(
    MEDIA_ROOT=TEST_MEDIA_ROOT,
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage",
)
class ListingWizardTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.user = get_user_model().objects.create_user("seller", password="secret123")
        self.client.force_login(self.user)
        self.url = reverse("listings:listing_create")
        self.base = {
            "title": "یک عنوان حرفه‌ای برای فروش دارایی دیجیتال",
            "description": "توضیحات کامل و شفاف درباره تاریخچه دارایی، مزیت رقابتی، شرایط فعلی و فرصت‌های رشد آینده. " * 2,
            "price": "25000000",
            "sale_type": "full_ownership",
        }

    def post(self, data):
        return self.client.post(self.url, data, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

    def test_every_selectable_category_has_unique_editable_schema(self):
        self.assertEqual(validate_category_config(), [])
        config = build_category_form_config()
        self.assertEqual(set(config), {slug for slug, _ in Category.PLATFORM_CHOICES})
        for schema in config.values():
            names = [item["name"] for item in schema["fields"]]
            self.assertEqual(len(names), len(set(names)))

    def test_get_renders_category_first_wizard(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-panel="category"')
        self.assertContains(response, 'name="category" id="category-input"')
        self.assertContains(response, "website_blog")
        for panel in ("finance", "analytics", "story", "ecosystem", "media"):
            self.assertContains(response, f'data-panel="{panel}"')
        for field_name in ("about_platform", "expense_count", "faq_count", "traffic_count",
                           "sale_include_count", "license_item_count", "service_count",
                           "social_count", "income_proof_count", "attachment_count",
                           "about_platform_css"):
            self.assertContains(response, f'name="{field_name}"')
        self.assertContains(response, 'id="about-preview"')

    def test_category_is_required_and_nothing_is_created(self):
        response = self.post({**self.base, "main_image": image_file()})
        self.assertEqual(response.status_code, 400)
        self.assertIn("category", response.json()["errors"])
        self.assertEqual(Listing.objects.count(), 0)

    def test_required_category_question_is_validated_server_side(self):
        response = self.post({**self.base, "category": "ecommerce_woocommerce", "main_image": image_file()})
        self.assertEqual(response.status_code, 400)
        self.assertIn("products_count", response.json()["errors"])
        self.assertEqual(Listing.objects.count(), 0)

    def test_activity_visits_and_transfer_process_are_optional(self):
        response = self.post({**self.base, "category": "website_blog", "main_image": image_file()})
        self.assertEqual(response.status_code, 200, response.content)
        listing = Listing.objects.get()
        self.assertEqual(listing.areas_activity, "")
        self.assertIsNone(listing.ownership_transfer_conditions)
        self.assertIsNone(WebsiteDetails.objects.get(listing=listing).monthly_visits)

    def test_website_listing_saves_canonical_metrics_and_detail_model(self):
        payload = {**self.base, "category": "website_blog", "monthly_visits": "12000",
                   "unique_visitors": "8000", "publishing_frequency": "12",
                   "is_income": "on", "monthly_income": "9000000", "main_image": image_file()}
        response = self.post(payload)
        self.assertEqual(response.status_code, 200, response.content)
        listing = Listing.objects.get()
        self.assertEqual(listing.asset_details["monthly_visits"], "12000")
        self.assertEqual(listing.asset_details["publishing_frequency"], "12")
        self.assertEqual(listing.monthly_income, 9000000)
        self.assertEqual(WebsiteDetails.objects.get(listing=listing).monthly_visits, 12000)

    def test_domain_flow_does_not_require_financial_data(self):
        payload = {**self.base, "category": "domain_com", "domain_name": "example.com",
                   "registrar": "Namecheap", "expiry_date": "2028-01-01",
                   "main_image": image_file("domain.png")}
        response = self.post(payload)
        self.assertEqual(response.status_code, 200, response.content)
        listing = Listing.objects.get()
        self.assertFalse(listing.is_income)
        self.assertIsNone(listing.monthly_income)
        self.assertEqual(DomainDetails.objects.get(listing=listing).domain_name, "example.com")

    def test_extended_category_sections_are_saved_without_duplicates(self):
        payload = {
            **self.base, "category": "website_blog", "monthly_visits": "12000",
            "is_income": "on", "monthly_income": "9000000", "main_image": image_file(),
            "about_platform": '<h2 class="intro">معرفی پلتفرم</h2><script>alert(1)</script><p>فرایند و فرصت رشد</p>',
            "about_platform_css": ".intro { color: #3157d5; position: fixed; }",
            "expense_count": "1", "exp_name_0": "سرور", "exp_amount_0": "500000", "exp_period_0": "monthly",
            "monetization_methods": ["banner_click_advertising"],
            "income_point_count": "1", "income_date_0": "2026-01-01", "income_val_0": "8000000",
            "views_point_count": "1", "views_date_0": "2026-01-01", "views_val_0": "11000",
            "traffic_count": "2", "trf_source_0": "organic_search", "trf_pct_0": "70",
            "trf_source_1": "direct", "trf_pct_1": "30",
            "sale_include_count": "2", "sale_include_0": "دامنه", "sale_include_1": "دامنه",
            "license_item_count": "1", "lic_name_0": "مجوز محتوا",
            "faq_count": "1", "faq_question_0": "زمان انتقال؟", "faq_answer_0": "سه روز کاری",
            "social_count": "1", "sm_platform_0": "instagram", "sm_followers_0": "1000", "sm_url_0": "https://instagram.com/example",
            "service_count": "2", "service_0": "Cloudflare", "service_1": "cloudflare",
            "tech_backend": ["django"], "tech_devops": ["docker"],
            "income_proof_count": "1", "income_proof_img_0": image_file("proof.png"), "income_proof_desc_0": "گزارش درگاه",
            "attachment_count": "1", "attachment_0": SimpleUploadedFile("report.txt", b"sample", content_type="text/plain"),
        }
        response = self.post(payload)
        self.assertEqual(response.status_code, 200, response.content)
        listing = Listing.objects.get()
        self.assertIn('<div class="aboutplatform-user-content">', listing.about_platform)
        self.assertIn("معرفی پلتفرم", listing.about_platform)
        self.assertIn(".aboutplatform-user-content .intro{color:#3157d5}", listing.about_platform)
        self.assertNotIn("script", listing.about_platform.lower())
        self.assertNotIn("position", listing.about_platform.lower())
        self.assertEqual(Expense.objects.filter(listing=listing).count(), 1)
        self.assertEqual(MonetizationMethod.objects.filter(listing=listing).count(), 1)
        self.assertEqual(IncomeDataPoint.objects.filter(listing=listing).count(), 1)
        self.assertEqual(ViewsDataPoint.objects.filter(listing=listing).count(), 1)
        self.assertEqual(TrafficSource.objects.filter(listing=listing).count(), 2)
        self.assertEqual(SaleInclude.objects.filter(listing=listing).count(), 1)
        self.assertEqual(License.objects.filter(listing=listing).count(), 1)
        self.assertEqual(ListingFAQ.objects.filter(listing=listing).count(), 1)
        self.assertEqual(SocialMedia.objects.filter(listing=listing).count(), 1)
        self.assertEqual(ServiceUsed.objects.filter(listing=listing).count(), 1)
        self.assertEqual(IncomeProof.objects.filter(listing=listing).count(), 1)
        self.assertEqual(Attachment.objects.filter(listing=listing).count(), 1)
        technology = TechnologyUsed.objects.get(listing=listing)
        self.assertEqual(technology.technology_backend, ["django"])
        self.assertEqual(technology.technology_devops, ["docker"])

    def test_optional_traffic_rejects_percentage_over_one_hundred(self):
        payload = {
            **self.base, "category": "website_blog", "main_image": image_file(),
            "traffic_count": "1", "trf_source_0": "direct", "trf_pct_0": "101",
        }
        response = self.post(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("trf_pct_0", response.json()["errors"])
        self.assertEqual(Listing.objects.count(), 0)

    def test_started_traffic_breakdown_must_total_one_hundred(self):
        payload = {
            **self.base, "category": "website_blog", "main_image": image_file(),
            "traffic_count": "1", "trf_source_0": "direct", "trf_pct_0": "70",
        }
        response = self.post(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("traffic_count", response.json()["errors"])
        self.assertEqual(Listing.objects.count(), 0)


class RichContentSanitizerTests(TestCase):
    def test_rich_content_is_scoped_and_dangerous_markup_is_removed(self):
        result = build_safe_rich_content(
            '<h2 onclick="bad()" style="color:red;position:fixed">عنوان</h2>'
            '<iframe src="https://example.com"></iframe><a href="javascript:bad()">لینک</a>',
            'body { color: red; } .card { background-color:#fff; background-image:url(https://bad.test/x); padding:12px; }',
        )
        self.assertIn('<h2 style="color:red">عنوان</h2>', result)
        self.assertIn('.aboutplatform-user-content .card{background-color:#fff;padding:12px}', result)
        for unsafe in ("onclick", "iframe", "javascript", "url(", "body{"):
            self.assertNotIn(unsafe, result.lower())
