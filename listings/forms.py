# listings/forms.py

from django import forms
from .models import Listing, IncomeProof, ListingImage

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['category', 'title', 'description', 'price', 'platform_url', 
                  'followers_count', 'monthly_income', 'main_image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'platform_url': forms.URLInput(attrs={'class': 'form-control'}),
            'followers_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'monthly_income': forms.NumberInput(attrs={'class': 'form-control'}),
            'main_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class IncomeProofForm(forms.ModelForm):
    class Meta:
        model = IncomeProof
        fields = ['proof_type', 'file', 'description']
        widgets = {
            'proof_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
