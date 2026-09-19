# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, UserProfile


class UserRegisterForm(UserCreationForm):
    """فرم ثبت‌نام کاربر جدید"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل خود را وارد کنید',
            'dir': 'ltr'
        })
    )
    phone_number = forms.CharField(
        max_length=11,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '09xxxxxxxxx',
            'dir': 'ltr'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({
            'placeholder': 'نام کاربری (بدون فاصله)',
            'dir': 'ltr'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'رمز عبور (حداقل 8 کاراکتر)'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'تکرار رمز عبور'
        })

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone.startswith('09'):
            raise forms.ValidationError('شماره موبایل باید با 09 شروع شود.')
        if not phone.isdigit():
            raise forms.ValidationError('شماره موبایل فقط باید شامل اعداد باشد.')
        if len(phone) != 11:
            raise forms.ValidationError('شماره موبایل باید 11 رقم باشد.')
        return phone


class UserLoginForm(AuthenticationForm):
    """فرم ورود"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({
            'placeholder': 'نام کاربری یا ایمیل',
            'dir': 'ltr'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'رمز عبور'
        })


class UserProfileBaseForm(forms.ModelForm):
    """فرم اطلاعات عمومی پروفایل"""
    class Meta:
        model = UserProfile
        fields = [
            'user_type', 'bio', 'address', 'city', 'province', 'postal_code',
            'email_address', 'iban_number', 'bank_name', 'tax_info'
        ]
        widgets = {
            'user_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'user_type_select'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'چند جمله درباره خودتان یا کسب‌وکارتان بنویسید'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'آدرس کامل شامل خیابان، پلاک و...'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: تهران'
            }),
            'province': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: تهران'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: 1234567890',
                'dir': 'ltr'
            }),
            'email_address': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیلی برای نمایش عمومی',
                'dir': 'ltr'
            }),
            'iban_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'IR + 24 رقم',
                'dir': 'ltr'
            }),
            'bank_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: بانک ملت'
            }),
            'tax_info': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شماره شناسه مالیاتی',
                'dir': 'ltr'
            }),
        }
        labels = {
            'user_type': 'نوع کاربر',
            'bio': 'بیو',
            'address': 'آدرس',
            'city': 'شهر',
            'province': 'استان',
            'postal_code': 'کد پستی',
            'email_address': 'ایمیل عمومی',
            'iban_number': 'شماره شبا',
            'bank_name': 'نام بانک',
            'tax_info': 'اطلاعات مالیاتی',
        }


class UserProfileUserForm(forms.ModelForm):
    """فرم اطلاعات کاربری (شماره موبایل، کد ملی، تصویر)"""
    national_code = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234567890',
            'dir': 'ltr'
        }),
        help_text='کد ملی باید 10 رقم باشد'
    )

    class Meta:
        model = User
        fields = ['phone_number', 'national_code', 'profile_image']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '09xxxxxxxxx',
                'dir': 'ltr'
            }),
            'profile_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'phone_number': 'شماره موبایل',
            'national_code': 'کد ملی',
            'profile_image': 'تصویر پروفایل',
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone and not phone.startswith('09'):
            raise forms.ValidationError('شماره موبایل باید با 09 شروع شود.')
        if phone and not phone.isdigit():
            raise forms.ValidationError('شماره موبایل فقط باید شامل اعداد باشد.')
        if phone and len(phone) != 11:
            raise forms.ValidationError('شماره موبایل باید 11 رقم باشد.')
        return phone

    def clean_national_code(self):
        code = self.cleaned_data.get('national_code')
        if code and len(code) != 10:
            raise forms.ValidationError('کد ملی باید 10 رقم باشد.')
        if code and not code.isdigit():
            raise forms.ValidationError('کد ملی فقط باید شامل اعداد باشد.')
        return code


class IndividualProfileForm(forms.ModelForm):
    """فرم اطلاعات شخص حقیقی"""
    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender',
            'national_id_image', 'selfie_with_id'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خانوادگی'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'national_id_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'selfie_with_id': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'date_of_birth': 'تاریخ تولد',
            'gender': 'جنسیت',
            'national_id_image': 'تصویر کارت ملی',
            'selfie_with_id': 'سلفی با مدرک',
        }


class CompanyProfileForm(forms.ModelForm):
    """فرم اطلاعات شخص حقوقی"""
    class Meta:
        model = UserProfile
        fields = [
            'company_name', 'company_type', 'registration_number',
            'economic_code', 'company_national_id', 'company_logo',
            'agent_name', 'agent_position', 'agent_national_code',
            'authorization_document'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام کامل شرکت'
            }),
            'company_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: شرکت سهامی خاص'
            }),
            'registration_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شماره ثبت از سازمان ثبت',
                'dir': 'ltr'
            }),
            'economic_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '14 رقمی',
                'dir': 'ltr'
            }),
            'company_national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شناسه ملی',
                'dir': 'ltr'
            }),
            'company_logo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'agent_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام کامل نماینده'
            }),
            'agent_position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: مدیر عامل'
            }),
            'agent_national_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '10 رقمی',
                'dir': 'ltr'
            }),
            'authorization_document': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,.pdf'
            }),
        }
        labels = {
            'company_name': 'نام شرکت',
            'company_type': 'نوع شرکت',
            'registration_number': 'شماره ثبت',
            'economic_code': 'کد اقتصادی',
            'company_national_id': 'شناسه ملی شرکت',
            'company_logo': 'لوگوی شرکت',
            'agent_name': 'نام نماینده',
            'agent_position': 'سمت نماینده',
            'agent_national_code': 'کد ملی نماینده',
            'authorization_document': 'مدرک نمایندگی',
        }


class SellerProfileForm(forms.ModelForm):
    """فرم اطلاعات فروشنده"""
    class Meta:
        model = UserProfile
        fields = ['business_category', 'business_license']
        widgets = {
            'business_category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: فروش آنلاین، خدمات و...'
            }),
            'business_license': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,.pdf'
            }),
        }
        labels = {
            'business_category': 'دسته‌بندی کسب‌وکار',
            'business_license': 'مجوز کسب‌وکار',
        }