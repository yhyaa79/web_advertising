# core/views.py

from django.shortcuts import render
from listings.models import Listing, Category

def home(request):
    active_listings = Listing.objects.filter(status='active')
    
    # ۱۰ آگهی جدید
    latest_listings = active_listings.order_by('-created_at')[:10]
    
    # ۱۰ آگهی پربازدید
    most_viewed_listings = active_listings.order_by('-views_count')[:10]
    
    # ۱۰ آگهی با بیشترین دنبال‌کننده
    most_followed_listings = active_listings.order_by('-followers_count')[:10]
    
    # ۱۰ قدیمی‌ترین پلتفرم‌ها (بر اساس سن پلتفرم)
    oldest_platforms = active_listings.order_by('-platform_age')[:10]
    
    # ۱۰ آگهی ارتقا یافته
    promoted_listings = active_listings.filter(is_preferment=True).order_by('-created_at')[:10]
    
    # ۱۰ آگهی مورد تایید
    verified_listings = active_listings.filter(is_verified=True).order_by('-created_at')[:10]
    
    # ۱۰ آگهی با بیشترین درآمد ماهیانه
    highest_income_listings = active_listings.filter(
        monthly_income__isnull=False
    ).order_by('-monthly_income')[:10]
    
    categories = Category.objects.all()
    
    context = {
        'latest_listings': latest_listings,
        'most_viewed_listings': most_viewed_listings,
        'most_followed_listings': most_followed_listings,
        'oldest_platforms': oldest_platforms,
        'promoted_listings': promoted_listings,
        'verified_listings': verified_listings,
        'highest_income_listings': highest_income_listings,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def load_more_listings(request):
    list_type = request.GET.get('type')
    offset = int(request.GET.get('offset', 10))
    limit = 10
    
    active_listings = Listing.objects.filter(status='active')
    
    if list_type == 'latest':
        listings = active_listings.order_by('-created_at')[offset:offset+limit]
    elif list_type == 'viewed':
        listings = active_listings.order_by('-views_count')[offset:offset+limit]
    elif list_type == 'followed':
        listings = active_listings.order_by('-followers_count')[offset:offset+limit]
    elif list_type == 'oldest':
        listings = active_listings.order_by('-platform_age')[offset:offset+limit]
    elif list_type == 'promoted':
        listings = active_listings.filter(is_preferment=True).order_by('-created_at')[offset:offset+limit]
    elif list_type == 'verified':
        listings = active_listings.filter(is_verified=True).order_by('-created_at')[offset:offset+limit]
    elif list_type == 'highest_income':
        listings = active_listings.filter(
            monthly_income__isnull=False
        ).order_by('-monthly_income')[offset:offset+limit]
    else:
        listings = []
        
    return render(request, 'core/partials/listing_cards.html', {'listings': listings})
