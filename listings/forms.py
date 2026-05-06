# listings/forms.py

from django import forms
from django.forms import inlineformset_factory
from .models import Listing, IncomeProof, ListingImage, VisitRequest

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['category', 'title', 'description', 'price', 'platform_url', 
                  'followers_count', 'monthly_income', 'main_image', 'is_private']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'platform_url': forms.URLInput(attrs={'class': 'form-control'}),
            'followers_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'monthly_income': forms.NumberInput(attrs={'class': 'form-control'}),
            'main_image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_private': 'آگهی خصوصی (نیاز به درخواست بازدید)',
        }

class IncomeProofForm(forms.ModelForm):
    class Meta:
        model = IncomeProof
        fields = ['image', 'description']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
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
