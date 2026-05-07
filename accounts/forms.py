# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, UserProfile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=11, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class UserProfileBaseForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'user_type', 'bio', 'address', 'city', 'province', 'postal_code',
            'email_address', 'iban_number', 'bank_name', 'tax_info'
        ]
        widgets = {
            'user_type': forms.Select(attrs={'class': 'form-control', 'id': 'user_type_select'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'province': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'email_address': forms.TextInput(attrs={'class': 'form-control'}),
            'iban_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tax_info': forms.TextInput(attrs={'class': 'form-control'}),
        }


class IndividualProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name','last_name', 'date_of_birth', 'gender', 'national_id_image', 'selfie_with_id']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'national_id_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'selfie_with_id': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'company_name', 'company_type', 'registration_number', 'economic_code',
            'company_national_id', 'company_logo', 'agent_name', 'agent_position',
            'agent_national_code', 'authorization_document'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_type': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control'}),
            'economic_code': forms.TextInput(attrs={'class': 'form-control'}),
            'company_national_id': forms.TextInput(attrs={'class': 'form-control'}),
            'company_logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'agent_name': forms.TextInput(attrs={'class': 'form-control'}),
            'agent_position': forms.TextInput(attrs={'class': 'form-control'}),
            'agent_national_code': forms.TextInput(attrs={'class': 'form-control'}),
            'authorization_document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['business_category', 'business_license']
        widgets = {
            'business_category': forms.TextInput(attrs={'class': 'form-control'}),
            'business_license': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
