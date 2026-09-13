# listings/admin.py

from django import forms
from django.contrib import admin
from .models import (
    Category, Listing, ListingAnalyst, SocialMedia, Attachment,
    SaleInclude, License, ConfirmedInformation, ServiceUsed,
    MonetizationMethod, Expense, IncomeDataPoint, ViewsDataPoint,
    ListingImage, VisitRequest, TechnologyUsed,
    # ← جدید: مدل‌های اختصاصی دسته‌بندی
    WebsiteDetails, EcommerceDetails, AppDetails, SocialMediaDetails,
    ContentMediaDetails, DomainDetails, ServiceBusinessDetails,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'get_platform_display_safe', 'get_main_category_display')
    list_filter   = ('platform',)
    search_fields = ('name',)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'platform':
            kwargs['choices'] = [
                (
                    main_label,
                    [(sub_slug, sub_label) for sub_slug, sub_label in subs],
                )
                for _main_slug, main_label, subs in Category.PLATFORM_CATEGORIES
            ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    @admin.display(description='برچسب پلتفرم')
    def get_platform_display_safe(self, obj):
        return obj.get_platform_display_safe()

    @admin.display(description='دسته اصلی')
    def get_main_category_display(self, obj):
        _, label = obj.get_platform_main_category()
        return label or '-'


# ── Inlines ──────────────────────────────────────────────────

class ListingAnalystInline(admin.StackedInline):
    model  = ListingAnalyst
    extra  = 0
    fields = ('analyst_name', 'analyst_expertise', 'analyst_education',
              'analyst_record', 'analyst_image', 'analyst_description')


class SocialMediaInline(admin.TabularInline):
    model  = SocialMedia
    extra  = 1
    fields = ('platform', 'followers', 'url')


class AttachmentInline(admin.TabularInline):
    model  = Attachment
    extra  = 1
    fields = ('file',)


class SaleIncludeInline(admin.TabularInline):
    model  = SaleInclude
    extra  = 1
    fields = ('asset_name',)


class LicenseInline(admin.TabularInline):
    model  = License
    extra  = 1
    fields = ('license_name',)


class ConfirmedInformationInline(admin.TabularInline):
    model  = ConfirmedInformation
    extra  = 1
    fields = ('confirmed_name',)


class ServiceUsedInline(admin.TabularInline):
    model  = ServiceUsed
    extra  = 1
    fields = ('service_name',)


class MonetizationMethodInline(admin.TabularInline):
    model  = MonetizationMethod
    extra  = 1
    fields = ('method',)


class ExpenseInline(admin.TabularInline):
    model  = Expense
    extra  = 1
    fields = ('expense_name', 'amount', 'period')


class IncomeDataPointInline(admin.TabularInline):
    model  = IncomeDataPoint
    extra  = 1
    fields = ('date', 'income')


class ViewsDataPointInline(admin.TabularInline):
    model  = ViewsDataPoint
    extra  = 1
    fields = ('date', 'views')


class ListingImageInline(admin.TabularInline):
    model  = ListingImage
    extra  = 1
    fields = ('image',)


class VisitRequestInline(admin.TabularInline):
    model           = VisitRequest
    extra           = 0
    readonly_fields = ('requester', 'message', 'status', 'created_at')
    fields          = ('requester', 'message', 'status', 'created_at')
    can_delete      = False

    def has_add_permission(self, request, obj=None):
        return False


# ═══════════════════════════════════════════════════════════════
#  Inlineهای اختصاصی دسته‌بندی (OneToOne)
# ═══════════════════════════════════════════════════════════════

class WebsiteDetailsInline(admin.StackedInline):
    model   = WebsiteDetails
    extra   = 0
    max_num = 1
    can_delete = False
    classes = ('collapse',)
    fieldsets = (
        ('اطلاعات ترافیک', {
            'fields': ('monthly_visits', 'unique_visitors', 'page_views',
                       'bounce_rate', 'avg_session_duration')
        }),
        ('سئو', {
            'fields': ('domain_authority', 'backlinks_count', 'pages_indexed',
                       'seo_score')
        }),
        ('محتوا و تکنولوژی', {
            'fields': ('tech_stack', 'content_count')
        }),
    )


class EcommerceDetailsInline(admin.StackedInline):
    model   = EcommerceDetails
    extra   = 0
    max_num = 1
    can_delete = False
    classes = ('collapse',)
    fieldsets = (
        ('فروش', {
            'fields': ('products_count', 'orders_per_month', 'aov',
                       'conversion_rate', 'cart_abandonment')
        }),
        ('مشتریان', {
            'fields': ('returning_customers', 'suppliers_count')
        }),
        ('انبار و ارسال', {
            'fields': ('inventory_value', 'has_inventory', 'shipping_partners')
        }),
    )


class AppDetailsInline(admin.StackedInline):
    model   = AppDetails
    extra   = 0
    max_num = 1
    can_delete = False
    classes = ('collapse',)
    fieldsets = (
        ('دانلودها', {
            'fields': ('downloads', 'active_installs')
        }),
        ('کاربران', {
            'fields': ('dau', 'mau', 'retention_rate')
        }),
        ('کیفیت', {
            'fields': ('rating', 'reviews_count', 'crash_rate')
        }),
        ('نسخه و درآمد', {
            'fields': ('current_version', 'last_update_date', 'has_in_app_purchase')
        }),
    )


class SocialMediaDetailsInline(admin.StackedInline):
    model   = SocialMediaDetails
    extra   = 0
    max_num = 1
    can_delete = False
    classes = ('collapse',)
    fieldsets = (
        ('اطلاعات پیج', {
            'fields': ('handle', 'followers', 'following', 'posts_count',
                       'has_verification')
        }),
        ('تعامل', {
            'fields': ('engagement_rate', 'avg_reach', 'avg_story_views',
                       'post_frequency')
        }),
        ('مخاطبان', {
            'fields': ('audience_country', 'audience_gender', 'audience_age_range')
        }),
        ('درآمد', {
            'fields': ('is_monetized',)
        }),
    )


class ContentMediaDetailsInline(admin.StackedInline):
    model   = ContentMediaDetails
    extra   = 0
    max_num = 1
    can_delete = False
    classes = ('collapse',)
    fieldsets = (
        ('اطلاعات محتوا', {
            'fields': ('content_type', 'subscribers', 'monthly_audience',
                       'episodes_count', 'publishing_frequency', 'platforms')
        }),
        ('تعامل', {
            'fields': ('avg_engagement', 'avg_downloads', 'open_rate', 'click_rate')
        }),
    )


class DomainDetailsInline(admin.StackedInline):
    model   = DomainDetails
    extra   = 0
    max_num = 1
    can_delete = False
    classes = ('collapse',)
    fieldsets = (
        ('اطلاعات دامنه', {
            'fields': ('domain_name', 'extension', 'registrar', 'expiry_date',
                       'domain_age_years')
        }),
        ('سئو و کلمه کلیدی', {
            'fields': ('keyword', 'search_volume', 'cpc', 'backlinks_count',
                       'monthly_type_in')
        }),
        ('ویژگی‌ها', {
            'fields': ('is_brandable', 'is_exact_match', 'has_history')
        }),
    )


class ServiceBusinessDetailsInline(admin.StackedInline):
    model   = ServiceBusinessDetails
    extra   = 0
    max_num = 1
    can_delete = False
    classes = ('collapse',)
    fieldsets = (
        ('خدمات', {
            'fields': ('services_list', 'team_size')
        }),
        ('مشتریان', {
            'fields': ('active_clients', 'total_clients', 'client_retention',
                       'contracts_count')
        }),
        ('مالی', {
            'fields': ('avg_project_value', 'monthly_projects',
                       'recurring_revenue_pct')
        }),
        ('ویژگی‌ها', {
            'fields': ('has_registered_brand', 'has_physical_office')
        }),
    )


# ── TechnologyUsed Admin Form ────────────────────────────────

class TechnologyUsedAdminForm(forms.ModelForm):
    technology_cms = forms.MultipleChoiceField(
        choices=TechnologyUsed.TECHNOLOGY_CHOICES_CMS,
        widget=forms.CheckboxSelectMultiple, required=False, label='CMS و فروشگاه‌ساز')
    technology_backend = forms.MultipleChoiceField(
        choices=TechnologyUsed.TECHNOLOGY_CHOICES_BACKEND,
        widget=forms.CheckboxSelectMultiple, required=False, label='تکنولوژی Backend')
    technology_frontend = forms.MultipleChoiceField(
        choices=TechnologyUsed.TECHNOLOGY_CHOICES_FRONTEND,
        widget=forms.CheckboxSelectMultiple, required=False, label='تکنولوژی Frontend')
    technology_database = forms.MultipleChoiceField(
        choices=TechnologyUsed.TECHNOLOGY_CHOICES_DATABASE,
        widget=forms.CheckboxSelectMultiple, required=False, label='تکنولوژی Database')
    technology_infrastructure = forms.MultipleChoiceField(
        choices=TechnologyUsed.TECHNOLOGY_CHOICES_INFRASTRUCTURE,
        widget=forms.CheckboxSelectMultiple, required=False, label='تکنولوژی Infrastructure')
    technology_mobile = forms.MultipleChoiceField(
        choices=TechnologyUsed.TECHNOLOGY_CHOICES_MOBILE,
        widget=forms.CheckboxSelectMultiple, required=False, label='تکنولوژی Mobile')
    technology_devops = forms.MultipleChoiceField(
        choices=TechnologyUsed.TECHNOLOGY_CHOICES_DEVOPS,
        widget=forms.CheckboxSelectMultiple, required=False, label='تکنولوژی DevOps')
    technology_third_party = forms.MultipleChoiceField(
        choices=TechnologyUsed.TECHNOLOGY_CHOICES_THIRD_PARTY,
        widget=forms.CheckboxSelectMultiple, required=False, label='سرویس‌های جانبی')

    class Meta:
        model  = TechnologyUsed
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            for field in [
                'technology_cms', 'technology_backend', 'technology_frontend',
                'technology_database', 'technology_infrastructure',
                'technology_mobile', 'technology_devops', 'technology_third_party',
            ]:
                self.fields[field].initial = getattr(self.instance, field) or []

    def _clean_list(self, key):
        return list(self.cleaned_data.get(key, []))

    def clean_technology_cms(self):            return self._clean_list('technology_cms')
    def clean_technology_backend(self):        return self._clean_list('technology_backend')
    def clean_technology_frontend(self):       return self._clean_list('technology_frontend')
    def clean_technology_database(self):       return self._clean_list('technology_database')
    def clean_technology_infrastructure(self): return self._clean_list('technology_infrastructure')
    def clean_technology_mobile(self):         return self._clean_list('technology_mobile')
    def clean_technology_devops(self):         return self._clean_list('technology_devops')
    def clean_technology_third_party(self):    return self._clean_list('technology_third_party')


class TechnologyUsedInline(admin.StackedInline):
    model   = TechnologyUsed
    form    = TechnologyUsedAdminForm
    extra   = 0
    max_num = 1
    fields  = (
        'technology_cms', 'technology_backend', 'technology_frontend',
        'technology_database', 'technology_infrastructure',
        'technology_mobile', 'technology_devops', 'technology_third_party',
    )


# ── ListingAdmin ─────────────────────────────────────────────

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'seller', 'category', 'sale_type',
        'price', 'discount_price', 'boost', 'premier',
        'is_private', 'status', 'created_at',
    )
    list_filter   = ('status', 'sale_type', 'boost', 'premier', 'is_private',
                     'is_verified', 'suggested_price', 'is_income', 'category', 'created_at')
    search_fields = ('title', 'description', 'seller__username')
    readonly_fields = ('views_count', 'created_at', 'updated_at')

    inlines = [
        # ── inlines اصلی
        ListingAnalystInline,
        SocialMediaInline,
        AttachmentInline,
        SaleIncludeInline,
        LicenseInline,
        ConfirmedInformationInline,
        ServiceUsedInline,
        MonetizationMethodInline,
        ExpenseInline,
        IncomeDataPointInline,
        ViewsDataPointInline,
        ListingImageInline,
        VisitRequestInline,
        TechnologyUsedInline,
        # ── inlines اختصاصی دسته‌بندی (فقط یکی پر می‌شود)
        WebsiteDetailsInline,
        EcommerceDetailsInline,
        AppDetailsInline,
        SocialMediaDetailsInline,
        ContentMediaDetailsInline,
        DomainDetailsInline,
        ServiceBusinessDetailsInline,
    ]

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('seller', 'title', 'category', 'description', 'location', 'about_platform')
        }),
        ('قیمت و تصویر', {
            'fields': ('price', 'discount_price', 'main_image')
        }),
        ('اطلاعات پلتفرم', {
            'fields': ('platform_url', 'areas_activity', 'followers_count',
                       'monthly_income', 'platform_age',
                       'most_like', 'most_view', 'most_comment')
        }),
        ('دلیل واگذاری', {
            'fields': ('sale_reason', 'sale_reason_description'),
        }),
        ('نوع فروش', {
            'fields': ('sale_type',),
        }),
        ('جزئیات: فروش مالکیت کامل', {
            'fields': ('ownership_document_status', 'ownership_transfer_conditions'),
            'classes': ('collapse',),
        }),
        ('جزئیات: فروش مالکیت بخشی / سهمی', {
            'fields': (
                'partial_ownership_percentage',
                'partial_ownership_valuation_method',
                'partial_ownership_buyer_rights',
                'partial_ownership_exit_conditions',
            ),
            'classes': ('collapse',),
        }),
        ('جزئیات: فروش مجوز / لایسنس', {
            'fields': (
                'license_duration_type', 'license_duration_months',
                'license_scope', 'license_restrictions',
            ),
            'classes': ('collapse',),
        }),
        ('جزئیات: فروش سهم از درآمد', {
            'fields': (
                'revenue_share_percentage', 'revenue_share_base',
                'revenue_share_payment_period', 'revenue_share_contract_duration',
                'revenue_share_minimum_guarantee',
            ),
            'classes': ('collapse',),
        }),
        ('جزئیات: فروش برند', {
            'fields': (
                'brand_transferred_assets', 'brand_legal_status',
                'brand_usage_restrictions', 'brand_industry_scope',
            ),
            'classes': ('collapse',),
        }),
        ('درآمد و هزینه', {
            'fields': (
                'total_revenue', 'total_profit',
                'avg_monthly_revenue', 'avg_monthly_profit',
                'profit_margin', 'profit_multiplier', 'revenue_multiplier',
                'post_sale_support',
            ),
            'classes': ('collapse',),
        }),
        ('تنظیمات', {
            'fields': ('boost', 'premier', 'suggested_price', 'is_income',
                       'is_verified', 'is_private', 'status', 'rejection_reason')
        }),
        ('آمار', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def get_queryset(self, request):
        # category یک CharField است، نه ForeignKey
        return super().get_queryset(request).select_related('seller')


@admin.register(VisitRequest)
class VisitRequestAdmin(admin.ModelAdmin):
    list_display  = ('listing', 'requester', 'status', 'created_at')
    list_filter   = ('status', 'created_at')
    search_fields = ('listing__title', 'requester__username', 'message')
    readonly_fields = ('created_at',)
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='approved')
        self.message_user(request, f'{updated} درخواست تایید شد.')
    approve_requests.short_description = 'تایید درخواست‌های انتخاب شده'

    def reject_requests(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f'{updated} درخواست رد شد.')
    reject_requests.short_description = 'رد درخواست‌های انتخاب شده'