# listings/admin.py

from django.contrib import admin
from .models import (
    Category, Listing, ListingAnalyst, SocialMedia, Attachment,
    SaleInclude, License, ConfirmedInformation, ServiceUsed, MonetizationMethod, Expense,
    IncomeDataPoint, ViewsDataPoint, ListingImage, VisitRequest, TechnologyUsed 
)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'platform')
    list_filter = ('platform',)
    search_fields = ('name',)


class ListingAnalystInline(admin.StackedInline):
    model = ListingAnalyst
    extra = 0
    fields = ('analyst_name', 'analyst_expertise', 'analyst_education', 'analyst_record', 'analyst_image', 'analyst_description')


class SocialMediaInline(admin.TabularInline):
    model = SocialMedia
    extra = 1
    fields = ('platform', 'followers', 'url')


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1
    fields = ('file',)


class SaleIncludeInline(admin.TabularInline):
    model = SaleInclude
    extra = 1
    fields = ('asset_name',)


class LicenseInline(admin.TabularInline):
    model = License
    extra = 1
    fields = ('license_name',)


class ConfirmedInformationInline(admin.TabularInline):
    model = ConfirmedInformation
    extra = 1
    fields = ('confirmed_name',)


class ServiceUsedInline(admin.TabularInline):
    model = ServiceUsed
    extra = 1
    fields = ('service_name',)


class MonetizationMethodInline(admin.TabularInline):
    model = MonetizationMethod
    extra = 1
    fields = ('method',)


class ExpenseInline(admin.TabularInline):
    model = Expense
    extra = 1
    fields = ('expense_name', 'amount', 'period')


class IncomeDataPointInline(admin.TabularInline):
    model = IncomeDataPoint
    extra = 1
    fields = ('date', 'income')


class ViewsDataPointInline(admin.TabularInline):
    model = ViewsDataPoint
    extra = 1
    fields = ('date', 'views')


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1
    fields = ('image',)


class VisitRequestInline(admin.TabularInline):
    model = VisitRequest
    extra = 0
    readonly_fields = ('requester', 'message', 'status', 'created_at')
    fields = ('requester', 'message', 'status', 'created_at')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


from django import forms
from django.contrib import admin
from .models import TechnologyUsed


class TechnologyUsedAdminForm(forms.ModelForm):
    """فرم سفارشی با MultipleChoiceField برای هر دسته"""

    technology_cms = forms.MultipleChoiceField(
        choices=TechnologyUsed.TECHNOLOGY_CHOICES_CMS,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='CMS و فروشگاه‌ساز'
    )
    technology_backend = forms.MultipleChoiceField(
        choices=TechnologyUsed.TECHNOLOGY_CHOICES_BACKEND,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='تکنولوژی Backend'
    )
    technology_frontend = forms.MultipleChoiceField(
        choices=TechnologyUsed.TECHNOLOGY_CHOICES_FRONTEND,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='تکنولوژی Frontend'
    )
    technology_database = forms.MultipleChoiceField(
        choices=TechnologyUsed.TECHNOLOGY_CHOICES_DATABASE,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='تکنولوژی Database'
    )
    technology_infrastructure = forms.MultipleChoiceField(
        choices=TechnologyUsed.TECHNOLOGY_CHOICES_INFRASTRUCTURE,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='تکنولوژی Infrastructure'
    )
    technology_mobile = forms.MultipleChoiceField(
        choices=TechnologyUsed.TECHNOLOGY_CHOICES_MOBILE,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='تکنولوژی Mobile'
    )
    technology_devops = forms.MultipleChoiceField(
        choices=TechnologyUsed.TECHNOLOGY_CHOICES_DEVOPS,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='تکنولوژی DevOps'
    )
    technology_third_party = forms.MultipleChoiceField(
        choices=TechnologyUsed.TECHNOLOGY_CHOICES_THIRD_PARTY,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='سرویس‌های جانبی'
    )

    class Meta:
        model = TechnologyUsed
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # مقادیر ذخیره‌شده رو به فرم برگردون
        if self.instance.pk:
            for field in [
                'technology_cms', 'technology_backend', 'technology_frontend',
                'technology_database', 'technology_infrastructure',
                'technology_mobile', 'technology_devops', 'technology_third_party'
            ]:
                self.fields[field].initial = getattr(self.instance, field) or []

    def clean_technology_cms(self):
        return list(self.cleaned_data.get('technology_cms', []))

    def clean_technology_backend(self):
        return list(self.cleaned_data.get('technology_backend', []))

    def clean_technology_frontend(self):
        return list(self.cleaned_data.get('technology_frontend', []))

    def clean_technology_database(self):
        return list(self.cleaned_data.get('technology_database', []))

    def clean_technology_infrastructure(self):
        return list(self.cleaned_data.get('technology_infrastructure', []))

    def clean_technology_mobile(self):
        return list(self.cleaned_data.get('technology_mobile', []))

    def clean_technology_devops(self):
        return list(self.cleaned_data.get('technology_devops', []))

    def clean_technology_third_party(self):
        return list(self.cleaned_data.get('technology_third_party', []))


class TechnologyUsedInline(admin.StackedInline):
    model = TechnologyUsed
    form = TechnologyUsedAdminForm
    extra = 0          # چون OneToOne هست، بیشتر از یکی نمی‌شه
    max_num = 1
    fields = (
        'technology_cms', 'technology_backend', 'technology_frontend',
        'technology_database', 'technology_infrastructure',
        'technology_mobile', 'technology_devops', 'technology_third_party'
    )




@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'seller', 
        'category', 
        'price', 
        'discount_price',
        'boost',
        'premier',
        'is_private',
        'status', 
        'created_at'
    )
    list_filter = ('status', 'boost', 'premier', 'is_private', 'is_verified', 'suggested_price', 'is_income', 'category', 'created_at')
    search_fields = ('title', 'description', 'seller__username')
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    
    inlines = [
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
    ]
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('seller', 'title', 'category', 'description', 'location', 'about_platform')
        }),
        ('قیمت و تصویر', {
            'fields': ('price', 'discount_price', 'main_image')
        }),
        ('اطلاعات پلتفرم', {
            'fields': ('platform_url', 'areas_activity', 'followers_count', 'monthly_income', 'platform_age', 'most_like', 'most_view', 'most_comment')
        }),
        ('درآمد و هزینه', {
            'fields': (
                'total_revenue', 'total_profit', 
                'avg_monthly_revenue', 'avg_monthly_profit',
                'profit_margin', 'profit_multiplier', 'revenue_multiplier',
                'post_sale_support'
            ),
            'classes': ('collapse',)
        }),
        ('تنظیمات', {
            'fields': ('boost', 'premier', 'suggested_price', 'is_income', 'is_verified', 'is_private', 'status', 'rejection_reason')
        }),
        ('آمار', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('seller', 'category')


@admin.register(VisitRequest)
class VisitRequestAdmin(admin.ModelAdmin):
    list_display = ('listing', 'requester', 'status', 'created_at')
    list_filter = ('status', 'created_at')
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
