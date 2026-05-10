# core/views.py

from django.shortcuts import render
from listings.models import Listing, Category

def home(request):
    # ابتدا تمام آگهی‌های فعال را می‌گیریم تا کدمان تمیزتر شود
    active_listings = Listing.objects.filter(status='active')
    
    # ۱. ۶ آگهی جدید (بهتر است بر اساس تاریخ ایجاد مرتب شوند)
    latest_listings = active_listings.order_by('-created_at')[:6]
    
    # ۲. ۶ آگهی پربازدید (مرتب‌سازی بر اساس فیلد بازدید)
    most_viewed_listings = active_listings.order_by('-views_count')[:6]
    
    # ۳. ۶ آگهی با بیشترین دنبال‌کننده (مرتب‌سازی بر اساس فیلد فالوورها)
    # توجه: نام فیلد 'followers_count' را بررسی کنید که در فایل models.py شما دقیقا چه نامی دارد
    most_followed_listings = active_listings.order_by('-followers_count')[:6]
    
    categories = Category.objects.all()
    
    context = {
        'latest_listings': latest_listings,
        'most_viewed_listings': most_viewed_listings,
        'most_followed_listings': most_followed_listings,  # ارسال لیست جدید به قالب
        'categories': categories,
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

from django.shortcuts import render
from listings.models import Listing

def load_more_listings(request):
    list_type = request.GET.get('type')
    offset = int(request.GET.get('offset', 6))
    limit = 6
    
    active_listings = Listing.objects.filter(status='active')
    
    if list_type == 'latest':
        listings = active_listings.order_by('-created_at')[offset:offset+limit]
    elif list_type == 'viewed':
        listings = active_listings.order_by('-views_count')[offset:offset+limit]
    elif list_type == 'followed':
        listings = active_listings.order_by('-followers_count')[offset:offset+limit]
    else:
        listings = []
        
    return render(request, 'core/partials/listing_cards.html', {'listings': listings})
