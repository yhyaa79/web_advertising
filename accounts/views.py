# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    UserRegisterForm,
    UserLoginForm,
    UserProfileBaseForm,
    IndividualProfileForm,
    CompanyProfileForm,
    SellerProfileForm
)
from .models import UserProfile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد!')
            return redirect('core:home')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'خوش آمدید!')
            return redirect('core:home')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'با موفقیت خارج شدید.')
    return redirect('core:home')


@login_required
def profile(request):
    profile_obj, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        base_form = UserProfileBaseForm(request.POST, instance=profile_obj)
        individual_form = IndividualProfileForm(request.POST, request.FILES, instance=profile_obj)
        company_form = CompanyProfileForm(request.POST, request.FILES, instance=profile_obj)
        seller_form = SellerProfileForm(request.POST, request.FILES, instance=profile_obj)

        user_type = request.POST.get('user_type', profile_obj.user_type)

        forms_are_valid = (
            base_form.is_valid() and
            seller_form.is_valid() and
            (
                individual_form.is_valid() if user_type == 'individual' else company_form.is_valid()
            )
        )

        if forms_are_valid:
            profile_instance = base_form.save(commit=False)

            # اطلاعات فروشنده
            profile_instance.business_category = seller_form.cleaned_data.get('business_category', '')

            if seller_form.cleaned_data.get('business_license'):
                profile_instance.business_license = seller_form.cleaned_data.get('business_license')

            if user_type == 'individual':
                # ذخیره فیلدهای حقیقی
                profile_instance.first_name = individual_form.cleaned_data.get('first_name')
                profile_instance.last_name = individual_form.cleaned_data.get('last_name')
                profile_instance.date_of_birth = individual_form.cleaned_data.get('date_of_birth')
                profile_instance.gender = individual_form.cleaned_data.get('gender', '')

                if individual_form.cleaned_data.get('national_id_image'):
                    profile_instance.national_id_image = individual_form.cleaned_data.get('national_id_image')

                if individual_form.cleaned_data.get('selfie_with_id'):
                    profile_instance.selfie_with_id = individual_form.cleaned_data.get('selfie_with_id')

                # پاک کردن فیلدهای حقوقی
                profile_instance.company_name = ''
                profile_instance.company_type = ''
                profile_instance.registration_number = ''
                profile_instance.economic_code = ''
                profile_instance.company_national_id = ''
                profile_instance.company_logo = None
                profile_instance.agent_name = ''
                profile_instance.agent_position = ''
                profile_instance.agent_national_code = ''
                profile_instance.authorization_document = None

            else:
                # ذخیره فیلدهای حقوقی
                profile_instance.company_name = company_form.cleaned_data.get('company_name', '')
                profile_instance.company_type = company_form.cleaned_data.get('company_type', '')
                profile_instance.registration_number = company_form.cleaned_data.get('registration_number', '')
                profile_instance.economic_code = company_form.cleaned_data.get('economic_code', '')
                profile_instance.company_national_id = company_form.cleaned_data.get('company_national_id', '')
                profile_instance.agent_name = company_form.cleaned_data.get('agent_name', '')
                profile_instance.agent_position = company_form.cleaned_data.get('agent_position', '')
                profile_instance.agent_national_code = company_form.cleaned_data.get('agent_national_code', '')

                if company_form.cleaned_data.get('company_logo'):
                    profile_instance.company_logo = company_form.cleaned_data.get('company_logo')

                if company_form.cleaned_data.get('authorization_document'):
                    profile_instance.authorization_document = company_form.cleaned_data.get('authorization_document')

                # پاک کردن فیلدهای حقیقی
                profile_instance.first_name = None
                profile_instance.last_name = None
                profile_instance.date_of_birth = None
                profile_instance.gender = ''
                profile_instance.national_id_image = None
                profile_instance.selfie_with_id = None

            profile_instance.save()

            messages.success(request, 'پروفایل با موفقیت به‌روزرسانی شد.')
            return redirect('accounts:profile')

    else:
        base_form = UserProfileBaseForm(instance=profile_obj)
        individual_form = IndividualProfileForm(instance=profile_obj)
        company_form = CompanyProfileForm(instance=profile_obj)
        seller_form = SellerProfileForm(instance=profile_obj)

    kyc_level = profile_obj.kyc_level
    kyc_class = 'kyc-0'

    if 0 < kyc_level <= 25:
        kyc_class = 'kyc-25'
    elif 25 < kyc_level <= 50:
        kyc_class = 'kyc-50'
    elif 50 < kyc_level <= 75:
        kyc_class = 'kyc-75'
    elif 75 < kyc_level <= 100:
        kyc_class = 'kyc-100'

    context = {
        'base_form': base_form,
        'individual_form': individual_form,
        'company_form': company_form,
        'seller_form': seller_form,
        'profile': profile_obj,
        'kyc_level': kyc_level,
        'kyc_class': kyc_class,
    }

    return render(request, 'accounts/profile.html', context)
