# listings/views.py

from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, F, Case, When, DecimalField
from .models import Listing, Category, IncomeProof, VisitRequest
from .forms import (ListingForm, IncomeProofFormSet, VisitRequestForm,
                    IncomeDataPointFormSet, ViewsDataPointFormSet, FAQFormSet)
import json
from notifications.utils import create_notification
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from accounts.models import SavedListing, ListingNote


User = get_user_model()

@property
def get_roi_display(self):
    if not self.monthly_income:
        return None
    
    price = self.discount_price if self.discount_price else self.price
    
    if not price:
        return None
    
    roi_months = price / self.monthly_income
    roi_years = roi_months / 12
    
    return f"{roi_months:.0f} ماه ({roi_years:.1f} سال)"


def listing_list(request):
    # تعریف متغیر پایه
    listings = Listing.objects.filter(status='active')
    
    # فیلتر دسته‌بندی
    category_id = request.GET.get('category')
    if category_id:
        listings = listings.filter(category_id=category_id)
    
    # جستجوی متنی
    search_query = request.GET.get('search')
    if search_query:
        listings = listings.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # فیلترهای چک‌باکسی
    filter_private = request.GET.get('filter_private')
    if filter_private:
        listings = listings.filter(is_private=True)
    
    filter_income = request.GET.get('filter_income')
    if filter_income:
        listings = listings.filter(is_income=True)
    
    filter_verified = request.GET.get('filter_verified')
    if filter_verified:
        listings = listings.filter(is_verified=True)
    
    filter_preferment = request.GET.get('filter_preferment')
    if filter_preferment:
        listings = listings.filter(boost=True)

    filter_premier = request.GET.get('filter_premier') 
    if filter_premier:
        listings = listings.filter(premier=True)
    
    # جستجوی پیشرفته - بازه قیمت
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        listings = listings.annotate(
            final_price=Case(
                When(discount_price__isnull=False, then=F('discount_price')),
                default=F('price'),
                output_field=DecimalField()
            )
        ).filter(final_price__gte=min_price)
    if max_price:
        listings = listings.annotate(
            final_price=Case(
                When(discount_price__isnull=False, then=F('discount_price')),
                default=F('price'),
                output_field=DecimalField()
            )
        ).filter(final_price__lte=max_price)
    
    # جستجوی پیشرفته - بازه سن پلتفرم
    min_age = request.GET.get('min_age')
    max_age = request.GET.get('max_age')
    if min_age:
        listings = listings.filter(platform_age__gte=min_age)
    if max_age:
        listings = listings.filter(platform_age__lte=max_age)
    
    # جستجوی پیشرفته - بازه دنبال‌کننده
    min_followers = request.GET.get('min_followers')
    max_followers = request.GET.get('max_followers')
    if min_followers:
        listings = listings.filter(followers_count__gte=min_followers)
    if max_followers:
        listings = listings.filter(followers_count__lte=max_followers)
    
    # جستجوی پیشرفته - بازه درآمد ماهیانه
    min_income = request.GET.get('min_income')
    max_income = request.GET.get('max_income')
    if min_income:
        listings = listings.filter(monthly_income__gte=min_income)
    if max_income:
        listings = listings.filter(monthly_income__lte=max_income)
    
    # دریافت آگهی‌های ویژه مرتبط با فیلترها
    boosted_listings = list(listings.filter(boost=True).order_by('?')[:3])
    
    # اگر کمتر از ۳ آگهی ویژه در این فیلتر پیدا شد، بقیه را از کل آگهی‌های ویژه سیستم پر کن
    if len(boosted_listings) < 3:
        needed = 3 - len(boosted_listings)
        current_boosted_ids = [item.id for item in boosted_listings]
        
        extra_boosted = Listing.objects.filter(
            status='active', 
            boost=True
        ).exclude(id__in=current_boosted_ids).order_by('?')[:needed]
        
        boosted_listings.extend(extra_boosted)

    # گرفتن آیدی تمام آگهی‌های ویژه برای حذف از لیست اصلی
    boosted_ids = [item.id for item in boosted_listings]
    
    # ایجاد لیست اصلی آگهی‌ها
    main_listings_queryset = listings.exclude(id__in=boosted_ids)

    # اعمال مرتب‌سازی
    sort_by = request.GET.get('sort_by')
    
    if sort_by == 'newest':
        main_listings_queryset = main_listings_queryset.order_by('-created_at')
    elif sort_by == 'oldest':
        main_listings_queryset = main_listings_queryset.order_by('created_at')
    elif sort_by == 'cheapest':
        main_listings_queryset = main_listings_queryset.annotate(
            final_price=Case(
                When(discount_price__isnull=False, then=F('discount_price')),
                default=F('price'),
                output_field=DecimalField()
            )
        ).order_by('final_price')
    elif sort_by == 'expensive':
        main_listings_queryset = main_listings_queryset.annotate(
            final_price=Case(
                When(discount_price__isnull=False, then=F('discount_price')),
                default=F('price'),
                output_field=DecimalField()
            )
        ).order_by('-final_price')
    else:
        main_listings_queryset = main_listings_queryset.order_by('-created_at')

    # صفحه‌بندی
    paginator = Paginator(main_listings_queryset, 20)
    page = request.GET.get('page')
    
    try:
        paginated_main_listings = paginator.page(page)
    except PageNotAnInteger:
        paginated_main_listings = paginator.page(1)
    except EmptyPage:
        paginated_main_listings = paginator.page(paginator.num_pages)
        
    categories = Category.objects.all()
    
    has_active_filters = any(
        request.GET.get(param) for param in ['search', 'category', 'sort_by', 'min_price', 'max_price']
    )

    # لیست آگهی‌های ذخیره شده کاربر
    saved_listing_ids = []
    if request.user.is_authenticated:
        saved_listing_ids = list(
            SavedListing.objects.filter(user=request.user).values_list('listing_id', flat=True)
        )

    context = {
        'boosted_listings': boosted_listings, 
        'listings': paginated_main_listings, 
        'categories': categories,
        'has_active_filters': has_active_filters,
        'saved_listing_ids': saved_listing_ids,
    }
    
    return render(request, 'listings/listing_list.html', context)


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    
    # صاحب آگهی همیشه دسترسی دارد
    if request.user.is_authenticated and request.user == listing.seller:
        has_access = True
    else:
        has_access = listing.has_access(request.user)
    
    visit_request = None
    if request.user.is_authenticated and listing.is_private and request.user != listing.seller:
        visit_request = VisitRequest.objects.filter(
            listing=listing,
            requester=request.user
        ).first()
    
    if has_access:
        listing.views_count += 1
        listing.save()
    
    income_proofs = listing.income_proofs.all() if has_access else []
    
    # داده‌های نمودار
    income_chart_data = None
    views_chart_data = None
    
    if has_access:
        income_data = listing.get_income_chart_data()
        if income_data:
            income_chart_data = json.dumps(income_data)
        
        views_data = listing.get_views_chart_data()
        if views_data:
            views_chart_data = json.dumps(views_data)
    
    similar_listings = Listing.objects.filter(
        category=listing.category, 
        status='active'
    ).exclude(pk=listing.pk)[:6]
    
    # بررسی ذخیره‌شده بودن آگهی و یادداشت کاربر
    is_saved = False
    user_note = None
    
    if request.user.is_authenticated:
        is_saved = SavedListing.objects.filter(user=request.user, listing=listing).exists()
        
        try:
            user_note = ListingNote.objects.get(user=request.user, listing=listing)
        except ListingNote.DoesNotExist:
            user_note = None
    
    context = {
        'listing': listing,
        'listings': similar_listings,
        'income_proofs': income_proofs,
        'has_access': has_access,
        'visit_request': visit_request,
        'income_chart_data': income_chart_data,
        'views_chart_data': views_chart_data,
        'is_saved': is_saved,
        'user_note': user_note,
    }
    return render(request, 'listings/listing_detail.html', context)




@login_required
def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        income_proof_formset = IncomeProofFormSet(request.POST, request.FILES)
        income_data_formset = IncomeDataPointFormSet(request.POST)
        views_data_formset = ViewsDataPointFormSet(request.POST)
        faq_formset = FAQFormSet(request.POST)

        if (form.is_valid() and income_proof_formset.is_valid() and
            income_data_formset.is_valid() and views_data_formset.is_valid() and
            faq_formset.is_valid()):

            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()

            income_proof_formset.instance = listing
            income_proof_formset.save()

            income_data_formset.instance = listing
            income_data_formset.save()

            views_data_formset.instance = listing
            views_data_formset.save()

            # ذخیره FAQ ها با فیلتر کردن رکوردهای خالی
            faqs = faq_formset.save(commit=False)
            for faq in faqs:
                # فقط FAQ هایی که question یا answer دارند را ذخیره کن
                if faq.question and faq.question.strip() and faq.answer and faq.answer.strip():
                    faq.listing = listing
                    faq.save()
            
            # حذف FAQ های marked for deletion
            for faq in faq_formset.deleted_objects:
                faq.delete()

            messages.success(request, 'آگهی شما با موفقیت ثبت شد و در انتظار تایید است.')
            return redirect('listings:my_listings')
    else:
        form = ListingForm()
        income_proof_formset = IncomeProofFormSet()
        income_data_formset = IncomeDataPointFormSet()
        views_data_formset = ViewsDataPointFormSet()
        faq_formset = FAQFormSet()

    return render(request, 'listings/listing_create.html', {
        'form': form,
        'income_proof_formset': income_proof_formset,
        'income_data_formset': income_data_formset,
        'views_data_formset': views_data_formset,
        'faq_formset': faq_formset,
    })



@login_required
def listing_edit(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        income_proof_formset = IncomeProofFormSet(request.POST, request.FILES, instance=listing)
        income_data_formset = IncomeDataPointFormSet(request.POST, instance=listing)
        views_data_formset = ViewsDataPointFormSet(request.POST, instance=listing)
        faq_formset = FAQFormSet(request.POST, instance=listing)

        if (form.is_valid() and income_proof_formset.is_valid() and
            income_data_formset.is_valid() and views_data_formset.is_valid() and
            faq_formset.is_valid()):

            form.save()
            income_proof_formset.save()
            income_data_formset.save()
            views_data_formset.save()
            faq_formset.save()

            messages.success(request, 'آگهی با موفقیت ویرایش شد.')
            return redirect('listings:listing_detail', pk=listing.pk)
    else:
        form = ListingForm(instance=listing)
        income_proof_formset = IncomeProofFormSet(instance=listing)
        income_data_formset = IncomeDataPointFormSet(instance=listing)
        views_data_formset = ViewsDataPointFormSet(instance=listing)
        faq_formset = FAQFormSet(instance=listing)

    return render(request, 'listings/listing_edit.html', {
        'form': form,
        'income_proof_formset': income_proof_formset,
        'income_data_formset': income_data_formset,
        'views_data_formset': views_data_formset,
        'faq_formset': faq_formset,
        'listing': listing
    })



@login_required
def my_listings(request):
    listings = Listing.objects.filter(seller=request.user)
    
    pending_requests = VisitRequest.objects.filter(
        listing__seller=request.user,
        status='pending'
    ).select_related('listing', 'requester')
    
    return render(request, 'listings/my_listings.html', {
        'listings': listings,
        'pending_requests': pending_requests
    })

@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete':
            listing.status = 'deleted'
            listing.save()
            messages.success(request, 'آگهی با موفقیت حذف شد.')
        elif action == 'sold':
            listing.status = 'sold'
            listing.save()
            messages.success(request, 'آگهی به عنوان فروخته شده علامت‌گذاری شد.')
        return redirect('listings:my_listings')
    
    return render(request, 'listings/listing_delete.html', {'listing': listing})

@login_required
def listing_activate(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    
    if listing.status == 'deleted':
        listing.status = 'pending'
        listing.save()
        messages.success(request, 'آگهی دوباره فعال شد و در انتظار تایید است.')
    
    return redirect('listings:my_listings')



@login_required
def request_visit(request, pk):
    listing = get_object_or_404(Listing, pk=pk, status='active')
    
    if not listing.is_private:
        messages.warning(request, 'این آگهی خصوصی نیست.')
        return redirect('listings:listing_detail', pk=pk)
    
    if request.user == listing.seller:
        messages.warning(request, 'شما صاحب این آگهی هستید.')
        return redirect('listings:listing_detail', pk=pk)
    
    existing_request = VisitRequest.objects.filter(
        listing=listing,
        requester=request.user
    ).first()
    
    if existing_request:
        if existing_request.status == 'approved':
            messages.info(request, 'درخواست شما قبلاً تایید شده است.')
        elif existing_request.status == 'pending':
            messages.info(request, 'درخواست شما در انتظار تایید است.')
        else:
            messages.warning(request, 'درخواست شما رد شده است.')
        return redirect('listings:listing_detail', pk=pk)
    
    if request.method == 'POST':
        form = VisitRequestForm(request.POST)
        if form.is_valid():
            visit_request = form.save(commit=False)
            visit_request.listing = listing
            visit_request.requester = request.user
            visit_request.save()
            
            # ایجاد اعلان برای فروشنده به صورت مستقیم
            create_notification(
                recipient=listing.seller,
                notification_type='visit_request',
                title='درخواست بازدید جدید',
                message=f'{request.user.username} برای آگهی "{listing.title}" درخواست بازدید ارسال کرده است.',
                action_url=reverse('listings:my_listings')
            )

            
            messages.success(request, 'درخواست بازدید شما ارسال شد و در انتظار تایید فروشنده است.')
            return redirect('listings:listing_detail', pk=pk)

    else:
        form = VisitRequestForm()
    
    return render(request, 'listings/request_visit.html', {
        'form': form,
        'listing': listing
    })

@login_required
def manage_visit_request(request, pk, action):
    visit_request = get_object_or_404(
        VisitRequest,
        pk=pk,
        listing__seller=request.user,
        status='pending'
    )

    listing_url = reverse('listings:listing_detail', kwargs={'pk': visit_request.listing.pk})
    
    if action == 'approve':
        visit_request.status = 'approved'
        visit_request.save()
        
        # ایجاد اعلان برای درخواست‌کننده
        create_notification(
            recipient=visit_request.requester,
            notification_type='visit_request',
            title='درخواست بازدید جدید',
            message=f'درخواست بازدید شما برای آگهی "{visit_request.listing.title}" تایید شد. اکنون می‌توانید جزئیات کامل را مشاهده کنید.',
            action_url=listing_url
        )
        
        messages.success(request, f'درخواست {visit_request.requester.username} تایید شد.')
    elif action == 'reject':
        visit_request.status = 'rejected'
        visit_request.save()
        
        # ایجاد اعلان برای درخواست‌کننده
        create_notification(
            recipient=visit_request.requester,
            notification_type='visit_request',
            title='درخواست بازدید جدید',
            message=f'متاسفانه درخواست بازدید شما برای آگهی "{visit_request.listing.title}" رد شد.',
            action_url=listing_url
        )
        
        messages.success(request, f'درخواست {visit_request.requester.username} رد شد.')
    
    return redirect('listings:my_listings')




def user_profile(request, username):
    """نمایش پروفایل عمومی کاربر"""
    profile_user = get_object_or_404(User, username=username)
    
    # آگهی‌های فعال کاربر
    user_listings = Listing.objects.filter(
        seller=profile_user,
        status='active'
    )
    
    # آمار کاربر
    total_listings = user_listings.count()
    total_views = sum(listing.views_count for listing in user_listings)
    
    context = {
        'profile_user': profile_user,
        'user_listings': user_listings,
        'total_listings': total_listings,
        'total_views': total_views,
    }
    
    return render(request, 'listings/user_profile.html', context)





@login_required
def similar_listings(request, pk):
    """نمایش آگهی‌های مشابه بر اساس معیارهای مختلف"""
    listing = get_object_or_404(Listing, pk=pk)
    
    # محاسبه قیمت نهایی آگهی اصلی
    base_price = listing.discount_price if listing.discount_price else listing.price
    
    # محاسبه ROI آگهی اصلی
    base_roi = None
    if listing.monthly_income and listing.monthly_income > 0:
        base_roi = float(base_price / listing.monthly_income)
    
    # فیلتر اولیه: همان دسته‌بندی و فعال
    similar = Listing.objects.filter(
        category=listing.category,
        status='active'
    ).exclude(pk=listing.pk)
    
    # محاسبه قیمت نهایی برای همه آگهی‌ها
    similar = similar.annotate(
        final_price=Case(
            When(discount_price__isnull=False, then=F('discount_price')),
            default=F('price'),
            output_field=DecimalField()
        )
    )
    
    # فیلتر بر اساس بازه قیمت (±30%)
    price_min = base_price * Decimal('0.7')
    price_max = base_price * Decimal('1.3') 
    similar = similar.filter(
        final_price__gte=price_min,
        final_price__lte=price_max
    )
    
    # فیلتر بر اساس تعداد دنبال‌کننده (±40%)
    if listing.followers_count > 0:
        followers_min = listing.followers_count * Decimal('0.6')
        followers_max = listing.followers_count * Decimal('1.4')
        similar = similar.filter(
            followers_count__gte=followers_min,
            followers_count__lte=followers_max
        )
    
    # فیلتر بر اساس سن پلتفرم (±2 سال)
    if listing.platform_age > 0:
        age_min = max(0, listing.platform_age - 3)
        age_max = listing.platform_age + 3
        similar = similar.filter(
            platform_age__gte=age_min,
            platform_age__lte=age_max
        )
    
    # فیلتر بر اساس ROI (±30%)
    if base_roi:
        similar = similar.filter(
            monthly_income__isnull=False,
            monthly_income__gt=0
        ).annotate(
            roi_months=F('final_price') / F('monthly_income')
        )
        
        roi_min = Decimal(str(base_roi)) * Decimal('0.7')
        roi_max = Decimal(str(base_roi)) * Decimal('1.3')
        similar = similar.filter(
            roi_months__gte=roi_min,
            roi_months__lte=roi_max
        )
    
    # مرتب‌سازی بر اساس اولویت آگهی پیشرفته و سپس شباهت (نزدیک‌ترین قیمت)
    similar = similar.order_by('-boost', 'final_price')[:12]
    
    categories = Category.objects.all()
    
    context = {
        'listings': similar,
        'base_listing': listing,
        'categories': categories,
        'is_similar_view': True,
    }
    
    return render(request, 'listings/listing_list.html', context)
