# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction

from .forms import (
    UserRegisterForm,
    UserLoginForm,
    UserProfileBaseForm,
    UserProfileUserForm,
    IndividualProfileForm,
    CompanyProfileForm,
    SellerProfileForm
)
from .models import User, UserProfile, SavedListing, ListingNote
from listings.models import Listing


# ════════════════════════════════════════════════════════════════
# احراز هویت (ثبت‌نام، ورود، خروج)
# ════════════════════════════════════════════════════════════════

def register(request):
    """ثبت‌نام کاربر جدید"""
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    # ایجاد پروفایل خودکار
                    UserProfile.objects.create(user=user)
                    login(request, user)
                    messages.success(request, '✓ ثبت‌نام با موفقیت انجام شد!')
                    return redirect('accounts:profile')
            except Exception as e:
                messages.error(request, f'خطا در ثبت‌نام: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def user_login(request):
    """ورود کاربر"""
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, '✓ خوش آمدید!')
            next_url = request.GET.get('next', 'core:home')
            return redirect(next_url)
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, 'accounts/login.html', context)


@login_required
def user_logout(request):
    """خروج کاربر"""
    logout(request)
    messages.info(request, '✓ با موفقیت خارج شدید.')
    return redirect('core:home')


# ════════════════════════════════════════════════════════════════
# پروفایل و اطلاعات کاربر
# ════════════════════════════════════════════════════════════════

@login_required
@transaction.atomic
def profile(request):
    """ویرایش پروفایل کاربر"""
    user = request.user
    profile_obj, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        # فرم‌ها
        user_form = UserProfileUserForm(request.POST, request.FILES, instance=user)
        base_form = UserProfileBaseForm(request.POST, instance=profile_obj)
        individual_form = IndividualProfileForm(request.POST, request.FILES, instance=profile_obj)
        company_form = CompanyProfileForm(request.POST, request.FILES, instance=profile_obj)
        seller_form = SellerProfileForm(request.POST, request.FILES, instance=profile_obj)

        # نوع کاربر
        user_type = request.POST.get('user_type', profile_obj.user_type)

        # اعتبارسنجی
        forms_are_valid = (
            user_form.is_valid() and
            base_form.is_valid() and
            seller_form.is_valid() and
            (
                individual_form.is_valid() if user_type == 'individual' else company_form.is_valid()
            )
        )

        if forms_are_valid:
            try:
                # ذخیره اطلاعات User
                user_form.save()

                # ذخیره اطلاعات پروفایل پایه
                profile_instance = base_form.save(commit=False)
                profile_instance.user_type = user_type

                # ذخیره اطلاعات فروشنده
                if seller_form.cleaned_data.get('business_category'):
                    profile_instance.business_category = seller_form.cleaned_data['business_category']
                
                if seller_form.cleaned_data.get('business_license'):
                    profile_instance.business_license = seller_form.cleaned_data['business_license']

                # پاک‌سازی و ذخیره بر اساس نوع کاربر
                if user_type == 'individual':
                    # اطلاعات شخص حقیقی
                    profile_instance.first_name = individual_form.cleaned_data.get('first_name', '')
                    profile_instance.last_name = individual_form.cleaned_data.get('last_name', '')
                    profile_instance.date_of_birth = individual_form.cleaned_data.get('date_of_birth')
                    profile_instance.gender = individual_form.cleaned_data.get('gender', '')

                    if individual_form.cleaned_data.get('national_id_image'):
                        profile_instance.national_id_image = individual_form.cleaned_data['national_id_image']

                    if individual_form.cleaned_data.get('selfie_with_id'):
                        profile_instance.selfie_with_id = individual_form.cleaned_data['selfie_with_id']

                    # پاک کردن اطلاعات شخص حقوقی
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

                else:  # company
                    # اطلاعات شخص حقوقی
                    profile_instance.company_name = company_form.cleaned_data.get('company_name', '')
                    profile_instance.company_type = company_form.cleaned_data.get('company_type', '')
                    profile_instance.registration_number = company_form.cleaned_data.get('registration_number', '')
                    profile_instance.economic_code = company_form.cleaned_data.get('economic_code', '')
                    profile_instance.company_national_id = company_form.cleaned_data.get('company_national_id', '')
                    profile_instance.agent_name = company_form.cleaned_data.get('agent_name', '')
                    profile_instance.agent_position = company_form.cleaned_data.get('agent_position', '')
                    profile_instance.agent_national_code = company_form.cleaned_data.get('agent_national_code', '')

                    if company_form.cleaned_data.get('company_logo'):
                        profile_instance.company_logo = company_form.cleaned_data['company_logo']

                    if company_form.cleaned_data.get('authorization_document'):
                        profile_instance.authorization_document = company_form.cleaned_data['authorization_document']

                    # پاک کردن اطلاعات شخص حقیقی
                    profile_instance.first_name = ''
                    profile_instance.last_name = ''
                    profile_instance.date_of_birth = None
                    profile_instance.gender = ''
                    profile_instance.national_id_image = None
                    profile_instance.selfie_with_id = None

                # ذخیره پروفایل
                profile_instance.save()

                messages.success(request, '✓ پروفایل با موفقیت به‌روزرسانی شد.')
                return redirect('accounts:profile')

            except Exception as e:
                messages.error(request, f'خطا در ذخیره‌سازی: {str(e)}')
        else:
            # نمایش خطاها
            all_errors = {}
            for form_obj in [user_form, base_form, individual_form, company_form, seller_form]:
                for field, errors in form_obj.errors.items():
                    if field not in all_errors:
                        all_errors[field] = []
                    all_errors[field].extend(errors)

            for field, errors in all_errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

    else:  # GET request
        user_form = UserProfileUserForm(instance=user)
        base_form = UserProfileBaseForm(instance=profile_obj)
        individual_form = IndividualProfileForm(instance=profile_obj)
        company_form = CompanyProfileForm(instance=profile_obj)
        seller_form = SellerProfileForm(instance=profile_obj)

    # محاسبه سطح احراز هویت
    kyc_level = profile_obj.kyc_level
    kyc_class = _get_kyc_class(kyc_level)

    context = {
        'user_form': user_form,
        'base_form': base_form,
        'individual_form': individual_form,
        'company_form': company_form,
        'seller_form': seller_form,
        'profile': profile_obj,
        'kyc_level': kyc_level,
        'kyc_class': kyc_class,
    }

    return render(request, 'accounts/profile.html', context)


def _get_kyc_class(kyc_level):
    """تعیین کلاس KYC بر اساس درصد"""
    if kyc_level == 0:
        return 'kyc-0'
    elif kyc_level <= 25:
        return 'kyc-25'
    elif kyc_level <= 50:
        return 'kyc-50'
    elif kyc_level <= 75:
        return 'kyc-75'
    else:
        return 'kyc-100'


# ════════════════════════════════════════════════════════════════
# آگهی‌های ذخیره شده
# ════════════════════════════════════════════════════════════════

@login_required
def saved_listings_view(request):
    """نمایش لیست آگهی‌های ذخیره شده کاربر"""
    saved_listings = SavedListing.objects.filter(
        user=request.user
    ).select_related('listing', 'listing__seller').order_by('-created_at')

    saved_listing_ids = list(
        SavedListing.objects.filter(user=request.user).values_list('listing_id', flat=True)
    )

    # دریافت تمام notes
    notes_dict = {}
    for note in ListingNote.objects.filter(user=request.user):
        notes_dict[note.listing_id] = note

    # ترکیب saved_listings با notes
    saved_with_notes = []
    for saved in saved_listings:
        note = notes_dict.get(saved.listing_id)
        saved_with_notes.append({
            'saved': saved,
            'note': note
        })

    context = {
        'saved_with_notes': saved_with_notes,
        'saved_listing_ids': saved_listing_ids,
        'count': len(saved_with_notes),
    }
    return render(request, 'accounts/saved_listings.html', context)


@login_required
@require_POST
def toggle_save_listing(request, listing_id):
    """ذخیره یا حذف آگهی از لیست ذخیره‌شده‌ها"""
    listing = get_object_or_404(Listing, pk=listing_id)
    
    try:
        saved_listing, created = SavedListing.objects.get_or_create(
            user=request.user,
            listing=listing
        )
        
        if not created:
            saved_listing.delete()
            is_saved = False
            message = 'آگهی از لیست ذخیره‌شده‌ها حذف شد'
        else:
            is_saved = True
            message = 'آگهی به لیست ذخیره‌شده‌ها اضافه شد'

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'is_saved': is_saved,
                'message': message
            })
        
        messages.success(request, message)
        
    except Exception as e:
        error_msg = f'خطا: {str(e)}'
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': error_msg
            }, status=400)
        messages.error(request, error_msg)

    return redirect('listings:listing_detail', pk=listing_id)


# ════════════════════════════════════════════════════════════════
# یادداشت‌های آگهی
# ════════════════════════════════════════════════════════════════

@login_required
@require_POST
def save_listing_note(request, listing_id):
    """ذخیره یا بروزرسانی یادداشت آگهی"""
    listing = get_object_or_404(Listing, pk=listing_id)
    note_text = request.POST.get('note', '').strip()

    if not note_text:
        error_msg = 'متن یادداشت نمی‌تواند خالی باشد'
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': error_msg
            }, status=400)
        messages.error(request, error_msg)
        return redirect('listings:listing_detail', pk=listing_id)

    if len(note_text) > 1000:
        error_msg = 'یادداشت نمی‌تواند بیشتر از 1000 کاراکتر باشد'
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': error_msg
            }, status=400)
        messages.error(request, error_msg)
        return redirect('listings:listing_detail', pk=listing_id)

    try:
        note, created = ListingNote.objects.update_or_create(
            user=request.user,
            listing=listing,
            defaults={'note': note_text}
        )

        message = 'یادداشت با موفقیت ذخیره شد' if created else 'یادداشت با موفقیت بروزرسانی شد'

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': message,
                'note': note.note,
                'updated_at': note.updated_at.strftime('%Y/%m/%d %H:%M'),
                'created': created
            })

        messages.success(request, message)

    except Exception as e:
        error_msg = f'خطا: {str(e)}'
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': error_msg
            }, status=400)
        messages.error(request, error_msg)

    return redirect('listings:listing_detail', pk=listing_id)


@login_required
@require_POST
def delete_listing_note(request, listing_id):
    """حذف یادداشت آگهی"""
    listing = get_object_or_404(Listing, pk=listing_id)
    
    try:
        note = ListingNote.objects.get(user=request.user, listing=listing)
        note.delete()
        message = 'یادداشت با موفقیت حذف شد'
        success = True
    except ListingNote.DoesNotExist:
        message = 'یادداشتی یافت نشد'
        success = False
    except Exception as e:
        message = f'خطا: {str(e)}'
        success = False

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': success,
            'message': message
        }, status=200 if success else 400)

    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)

    return redirect('listings:listing_detail', pk=listing_id)