# listings/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Listing, Category, IncomeProof, VisitRequest
from .forms import (ListingForm, IncomeProofFormSet, VisitRequestForm, 
                    IncomeDataPointFormSet, ViewsDataPointFormSet)
import json
from notifications.utils import notify_visit_request, notify_visit_approved, notify_visit_rejected
from django.contrib.auth import get_user_model

User = get_user_model()

def listing_list(request):
    listings = Listing.objects.filter(status='active')
    
    category_id = request.GET.get('category')
    if category_id:
        listings = listings.filter(category_id=category_id)
    

    
    search_query = request.GET.get('search')
    if search_query:
        listings = listings.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    categories = Category.objects.all()
    
    context = {
        'listings': listings,
        'categories': categories,
    }
    return render(request, 'listings/listing_list.html', context)

# listings/views.py

def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    
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
            
    # --- کدهای اضافه شده برای رفع مشکل ---
    # پیدا کردن آگهی‌های مشابه (مثلا ۳ آگهی فعال در همان دسته‌بندی به جز آگهی فعلی)
    similar_listings = Listing.objects.filter(
        category=listing.category, 
        status='active'
    ).exclude(pk=listing.pk)[:6]
    # -------------------------------------
    
    context = {
        'listing': listing,
        'listings': similar_listings, # این خط باید اضافه شود
        'income_proofs': income_proofs,
        'has_access': has_access,
        'visit_request': visit_request,
        'income_chart_data': income_chart_data,
        'views_chart_data': views_chart_data,
    }
    return render(request, 'listings/listing_detail.html', context)



@login_required
def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        income_proof_formset = IncomeProofFormSet(request.POST, request.FILES)
        income_data_formset = IncomeDataPointFormSet(request.POST)
        views_data_formset = ViewsDataPointFormSet(request.POST)
        
        if (form.is_valid() and income_proof_formset.is_valid() and 
            income_data_formset.is_valid() and views_data_formset.is_valid()):
            
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            
            income_proof_formset.instance = listing
            income_proof_formset.save()
            
            income_data_formset.instance = listing
            income_data_formset.save()
            
            views_data_formset.instance = listing
            views_data_formset.save()
            
            messages.success(request, 'آگهی شما با موفقیت ثبت شد و در انتظار تایید است.')
            return redirect('listings:my_listings')
    else:
        form = ListingForm()
        income_proof_formset = IncomeProofFormSet()
        income_data_formset = IncomeDataPointFormSet()
        views_data_formset = ViewsDataPointFormSet()
    
    return render(request, 'listings/listing_create.html', {
        'form': form,
        'income_proof_formset': income_proof_formset,
        'income_data_formset': income_data_formset,
        'views_data_formset': views_data_formset,
    })

@login_required
def listing_edit(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        income_proof_formset = IncomeProofFormSet(request.POST, request.FILES, instance=listing)
        income_data_formset = IncomeDataPointFormSet(request.POST, instance=listing)
        views_data_formset = ViewsDataPointFormSet(request.POST, instance=listing)
        
        if (form.is_valid() and income_proof_formset.is_valid() and 
            income_data_formset.is_valid() and views_data_formset.is_valid()):
            
            form.save()
            income_proof_formset.save()
            income_data_formset.save()
            views_data_formset.save()
            
            messages.success(request, 'آگهی با موفقیت ویرایش شد.')
            return redirect('listings:listing_detail', pk=listing.pk)
    else:
        form = ListingForm(instance=listing)
        income_proof_formset = IncomeProofFormSet(instance=listing)
        income_data_formset = IncomeDataPointFormSet(instance=listing)
        views_data_formset = ViewsDataPointFormSet(instance=listing)
    
    return render(request, 'listings/listing_edit.html', {
        'form': form,
        'income_proof_formset': income_proof_formset,
        'income_data_formset': income_data_formset,
        'views_data_formset': views_data_formset,
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
            
            # ایجاد اعلان برای فروشنده
            notify_visit_request(visit_request)
            
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
    
    if action == 'approve':
        visit_request.status = 'approved'
        visit_request.save()
        
        # ایجاد اعلان برای درخواست‌کننده
        notify_visit_approved(visit_request)
        
        messages.success(request, f'درخواست {visit_request.requester.username} تایید شد.')
    elif action == 'reject':
        visit_request.status = 'rejected'
        visit_request.save()
        
        # ایجاد اعلان برای درخواست‌کننده
        notify_visit_rejected(visit_request)
        
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
