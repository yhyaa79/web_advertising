# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'phone_number', 'national_code', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'is_staff', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'phone_number', 'national_code']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('اطلاعات تکمیلی', {
            'fields': ('phone_number', 'national_code', 'profile_image', 'is_verified')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('اطلاعات تکمیلی', {
            'fields': ('phone_number', 'national_code', 'profile_image', 'is_verified')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'kyc_level', 'city', 'province']
    list_filter = ['user_type', 'kyc_level', 'province']
    search_fields = ['user__username', 'user__email', 'company_name', 'national_id_image']
    
    fieldsets = (
        ('کاربر', {
            'fields': ('user', 'user_type')
        }),
        ('اطلاعات عمومی', {
            'fields': ('bio', 'address', 'email_address', 'city', 'province', 'postal_code')
        }),
        ('اطلاعات شخص حقیقی', {
            'fields': ('first_name','last_name', 'date_of_birth', 'gender', 'national_id_image', 'selfie_with_id'),
            'classes': ('collapse',)
        }),
        ('اطلاعات شخص حقوقی', {
            'fields': ('company_name', 'company_type', 'registration_number', 'economic_code', 
                      'company_national_id', 'company_logo'),
            'classes': ('collapse',)
        }),
        ('نماینده شرکت', {
            'fields': ('agent_name', 'agent_position', 'agent_national_code', 'authorization_document'),
            'classes': ('collapse',)
        }),
        ('اطلاعات مالی', {
            'fields': ('iban_number', 'bank_name', 'tax_info')
        }),
        ('اطلاعات فروشنده', {
            'fields': ('business_category', 'business_license'),
            'classes': ('collapse',)
        }),
        ('وضعیت', {
            'fields': ('kyc_level',)
        }),

    )
    
    readonly_fields = ['updated_at']
