# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True, verbose_name='شماره موبایل')
    national_code = models.CharField(max_length=10, unique=True, null=True, blank=True, verbose_name='کد ملی')
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True, verbose_name='تصویر پروفایل')
    is_verified = models.BooleanField(default=False, verbose_name='احراز شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ عضویت')

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('individual', 'شخص حقیقی'),
        ('company', 'شخص حقوقی'),
    )

    GENDER_CHOICES = (
        ('male', 'مرد'),
        ('female', 'زن'),
        ('other', 'سایر'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='کاربر')

    # عمومی
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='individual', verbose_name='نوع کاربر')
    bio = models.TextField(blank=True, verbose_name='بیو')
    address = models.TextField(blank=True, verbose_name='آدرس')
    email_address = models.EmailField(max_length=150, blank=True, null=True, verbose_name="ایمیل عمومی")
    city = models.CharField(max_length=100, blank=True, verbose_name='شهر')
    province = models.CharField(max_length=100, blank=True, verbose_name='استان')
    postal_code = models.CharField(max_length=20, blank=True, verbose_name='کد پستی')

    # حقیقی
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='نام')
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='نام خانوادگی')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, verbose_name='جنسیت')
    national_id_image = models.ImageField(upload_to='documents/national_ids/', null=True, blank=True, verbose_name='تصویر کارت ملی')
    selfie_with_id = models.ImageField(upload_to='documents/selfies/', null=True, blank=True, verbose_name='سلفی با مدرک')

    # حقوقی
    company_name = models.CharField(max_length=255, blank=True, verbose_name='نام شرکت')
    company_type = models.CharField(max_length=100, blank=True, verbose_name='نوع شرکت')
    registration_number = models.CharField(max_length=50, blank=True, verbose_name='شماره ثبت')
    economic_code = models.CharField(max_length=50, blank=True, verbose_name='کد اقتصادی')
    company_national_id = models.CharField(max_length=20, blank=True, verbose_name='شناسه ملی شرکت')
    company_logo = models.ImageField(upload_to='companies/logos/', null=True, blank=True, verbose_name='لوگوی شرکت')

    # نماینده شرکت
    agent_name = models.CharField(max_length=255, blank=True, verbose_name='نام نماینده')
    agent_position = models.CharField(max_length=255, blank=True, verbose_name='سمت نماینده')
    agent_national_code = models.CharField(max_length=10, blank=True, verbose_name='کد ملی نماینده')
    authorization_document = models.FileField(
        upload_to='documents/company_authorizations/',
        null=True,
        blank=True,
        verbose_name='مدرک نمایندگی'
    )

    # مالی
    iban_number = models.CharField(max_length=26, blank=True, verbose_name='شماره شبا')
    bank_name = models.CharField(max_length=100, blank=True, verbose_name='نام بانک')
    tax_info = models.CharField(max_length=255, blank=True, verbose_name='اطلاعات مالیاتی')

    # فروشنده
    business_category = models.CharField(max_length=255, blank=True, verbose_name='دسته‌بندی کسب‌وکار')
    business_license = models.FileField(upload_to='documents/licenses/', null=True, blank=True, verbose_name='مجوز کسب‌وکار')

    # وضعیت
    kyc_level = models.IntegerField(default=0, verbose_name='سطح احراز هویت')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')

    pro = models.BooleanField(default=False, verbose_name='کاربر پرو')
    premium = models.BooleanField(default=False, verbose_name='کاربر ویژه')

    def __str__(self):
        return f'پروفایل {self.user.username}'

    def calculate_kyc_level(self):
        score = 0
        total = 0

        common_fields = [
            self.address,
            self.city,
            self.province,
            self.postal_code,
            self.iban_number,
            self.bank_name,
        ]

        total += len(common_fields)
        score += sum(1 for field in common_fields if field)

        if self.user_type == 'individual':
            individual_fields = [
                self.first_name,
                self.last_name,
                self.date_of_birth,
                self.gender,
                self.national_id_image,
                self.selfie_with_id,
            ]
            total += len(individual_fields)
            score += sum(1 for field in individual_fields if field)

        elif self.user_type == 'company':
            company_fields = [
                self.company_name,
                self.company_type,
                self.registration_number,
                self.economic_code,
                self.company_national_id,
                self.agent_name,
                self.agent_position,
                self.agent_national_code,
                self.authorization_document,
            ]
            total += len(company_fields)
            score += sum(1 for field in company_fields if field)

        self.kyc_level = int((score / total) * 100) if total else 0
        return self.kyc_level

    def save(self, *args, **kwargs):
        self.calculate_kyc_level()
        super().save(*args, **kwargs)


class SavedListing(models.Model):
    """مدل برای ذخیره آگهی‌های مورد علاقه کاربر"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_listings', verbose_name='کاربر')
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='saved_by_users', verbose_name='آگهی')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ذخیره')

    class Meta:
        unique_together = ('user', 'listing')
        ordering = ['-created_at']
        verbose_name = 'آگهی ذخیره شده'
        verbose_name_plural = 'آگهی‌های ذخیره شده'

    def __str__(self):
        return f'{self.user.username} - {self.listing.title}'


class ListingNote(models.Model):
    """مدل برای یادداشت‌های شخصی کاربر برای هر آگهی"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listing_notes', verbose_name='کاربر')
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='user_notes', verbose_name='آگهی')
    note = models.TextField(verbose_name='یادداشت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        unique_together = ('user', 'listing')
        ordering = ['-updated_at']
        verbose_name = 'یادداشت آگهی'
        verbose_name_plural = 'یادداشت‌های آگهی'

    def __str__(self):
        return f'یادداشت {self.user.username} برای {self.listing.title}'
