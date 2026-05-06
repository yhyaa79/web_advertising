# listings/forms.py

from django import forms
from django.forms import inlineformset_factory
from .models import Listing, IncomeProof, ListingImage, VisitRequest, IncomeDataPoint, ViewsDataPoint

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['category', 'title', 'description', 'location', 'price', 'discount_price', 'platform_url', 
                  'followers_count', 'monthly_income', 'platform_age', 'most_like', 'most_view', 'most_comment', 
                  'main_image', 'is_private', 'is_income']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'platform_url': forms.URLInput(attrs={'class': 'form-control'}),
            'followers_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'monthly_income': forms.NumberInput(attrs={'class': 'form-control'}),
            'platform_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'most_like': forms.NumberInput(attrs={'class': 'form-control'}),
            'most_view': forms.NumberInput(attrs={'class': 'form-control'}),
            'most_comment': forms.NumberInput(attrs={'class': 'form-control'}),
            'main_image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_income': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_verified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_preferment': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'category': 'دسته بندی',
            'title': 'تیتر',
            'description': 'توضیحات',
            'location': 'موقعیت مکانی',
            'price': 'قیمت پایه',
            'discount_price': 'قیمت تخفیف خورده',
            'platform_url': 'ادرس پلتفرم',
            'followers_count': 'دنبال کنندگان',
            'monthly_income': 'درامد ماهیانه',
            'platform_age': 'سن پلتفرم',
            'most_like': 'بیشترین لایک',
            'most_view': 'بیشترین بازدید',
            'most_comment': 'بیشترین نظرات',
            'main_image': 'عکس اصلی',
            'is_private': 'اگهی خصوصی',
            'is_income': 'درامد داشتن اگهی',
            'is_verified': 'اگهی مورد تایید',
            'is_preferment': 'ارتقا اگهی ',
        }

class IncomeProofForm(forms.ModelForm):
    class Meta:
        model = IncomeProof
        fields = ['image', 'description']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class IncomeDataPointForm(forms.ModelForm):
    class Meta:
        model = IncomeDataPoint
        fields = ['date', 'income']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'income': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مثال: 5000000'}),
        }
        labels = {
            'date': 'تاریخ',
            'income': 'درآمد (تومان)',
        }

class ViewsDataPointForm(forms.ModelForm):
    class Meta:
        model = ViewsDataPoint
        fields = ['date', 'views']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'views': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مثال: 15000'}),
        }
        labels = {
            'date': 'تاریخ',
            'views': 'تعداد بازدید',
        }

class VisitRequestForm(forms.ModelForm):
    class Meta:
        model = VisitRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'لطفاً دلیل درخواست بازدید خود را بنویسید...'
            }),
        }
        labels = {
            'message': 'پیام درخواست',
        }

# Formset برای اثبات درآمد
IncomeProofFormSet = inlineformset_factory(
    Listing,
    IncomeProof,
    form=IncomeProofForm,
    extra=0,
    can_delete=True,
    max_num=10
)

# Formset برای نقاط داده درآمد
IncomeDataPointFormSet = inlineformset_factory(
    Listing,
    IncomeDataPoint,
    form=IncomeDataPointForm,
    extra=0,
    can_delete=True,
    max_num=50
)

# Formset برای نقاط داده بازدید
ViewsDataPointFormSet = inlineformset_factory(
    Listing,
    ViewsDataPoint,
    form=ViewsDataPointForm,
    extra=0,
    can_delete=True,
    max_num=50
)
