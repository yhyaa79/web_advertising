# listings/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Listing, Category, IncomeProof
from .forms import ListingForm, IncomeProofForm

def listing_list(request):
    listings = Listing.objects.filter(status='active')
    
    # فیلتر بر اساس دسته‌بندی
    category_id = request.GET.get('category')
    if category_id:
        listings = listings.filter(category_id=category_id)
    
    # جستجو
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

def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    listing.views_count += 1
    listing.save()
    
    income_proofs = listing.income_proofs.all()
    
    context = {
        'listing': listing,
        'income_proofs': income_proofs,
    }
    return render(request, 'listings/listing_detail.html', context)

@login_required
def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            messages.success(request, 'آگهی شما با موفقیت ثبت شد و در انتظار تایید است.')
            return redirect('listings:my_listings')
    else:
        form = ListingForm()
    
    return render(request, 'listings/listing_create.html', {'form': form})

@login_required
def listing_edit(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'آگهی با موفقیت ویرایش شد.')
            return redirect('listings:listing_detail', pk=listing.pk)
    else:
        form = ListingForm(instance=listing)
    
    return render(request, 'listings/listing_edit.html', {'form': form, 'listing': listing})

@login_required
def my_listings(request):
    listings = Listing.objects.filter(seller=request.user)
    return render(request, 'listings/my_listings.html', {'listings': listings})

@login_required
def add_income_proof(request, listing_pk):
    listing = get_object_or_404(Listing, pk=listing_pk, seller=request.user)
    
    if request.method == 'POST':
        form = IncomeProofForm(request.POST, request.FILES)
        if form.is_valid():
            proof = form.save(commit=False)
            proof.listing = listing
            proof.save()
            messages.success(request, 'اثبات درآمد با موفقیت اضافه شد.')
            return redirect('listings:listing_detail', pk=listing.pk)
    else:
        form = IncomeProofForm()
    
    return render(request, 'listings/add_income_proof.html', {'form': form, 'listing': listing})
