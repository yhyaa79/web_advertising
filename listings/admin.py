# listings/admin.py
from django.contrib import admin
from .models import Category, Listing, IncomeProof, ListingImage, VisitRequest

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class IncomeProofInline(admin.TabularInline):
    model = IncomeProof
    extra = 1
    readonly_fields = ('uploaded_at',)

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

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'seller', 
        'location',
        'category', 
        'price', 
        'discount_price', 
        'platform_url',
        'followers_count',
        'monthly_income',
        'platform_age',
        'most_like',
        'most_view',
        'most_comment',
        'is_preferment',
        'is_income',
        'is_verified',
        'is_private',
        'status', 
        'views_count', 
        'created_at'
    )
    list_filter = ('status','is_preferment', 'is_private', 'category', 'created_at')
    search_fields = ('title', 'description', 'seller__username')
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    inlines = [IncomeProofInline, ListingImageInline, VisitRequestInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('seller', 'title', 'category', 'description', 'location')
        }),
        ('قیمت و تصویر', {
            'fields': ('is_income', 'is_verified', 'price', 'discount_price', 'main_image')
        }),
        ('اطلاعات پلتفرم', {
            'fields': ('platform_url', 'followers_count', 'monthly_income', 'platform_age', 'most_like', 'most_view', 'most_comment', 'about_platform')
        }),
        ('تنظیمات', {
            'fields': ('is_preferment', 'is_private', 'status', 'rejection_reason')
        }),
        ('آمار', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('seller', 'category')

@admin.register(IncomeProof)
class IncomeProofAdmin(admin.ModelAdmin):
    list_display = ('listing', 'description', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('listing__title', 'description')
    readonly_fields = ('uploaded_at',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('listing')

@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ('listing', 'image')
    search_fields = ('listing__title',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('listing')

@admin.register(VisitRequest)
class VisitRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'listing_title',
        'listing_is_private',
        'requester',
        'status',
        'created_at'
    )
    list_filter = ('status', 'created_at', 'listing__is_private')
    search_fields = (
        'listing__title', 
        'requester__username', 
        'message'
    )
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('اطلاعات درخواست', {
            'fields': ('listing', 'requester', 'status')
        }),
        ('پیام', {
            'fields': ('message',)
        }),
        ('زمان', {
            'fields': ('created_at',)
        }),
    )
    
    def listing_title(self, obj):
        return obj.listing.title
    listing_title.short_description = 'عنوان آگهی'
    listing_title.admin_order_field = 'listing__title'
    
    def listing_is_private(self, obj):
        return obj.listing.is_private
    listing_is_private.short_description = 'خصوصی'
    listing_is_private.boolean = True
    listing_is_private.admin_order_field = 'listing__is_private'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('listing', 'requester')
    
    actions = ['approve_requests', 'reject_requests']
    
    def approve_requests(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='approved')
        self.message_user(request, f'{updated} درخواست تایید شد.')
    approve_requests.short_description = 'تایید درخواست‌های انتخاب شده'
    
    def reject_requests(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f'{updated} درخواست رد شد.')
    reject_requests.short_description = 'رد درخواست‌های انتخاب شده'


