# core/views.py

from django.shortcuts import render
from listings.models import Listing, Category
from django.views.generic import TemplateView 

class ComingSoonView(TemplateView):
    template_name = 'coming_soon.html'

def home(request):
    # گرفتن 5 آگهی آخر (در صورت نیاز فیلترهای دلخواه مثل is_active=True را اضافه کنید)
    latest_listings = Listing.objects.order_by('-created_at')[:5]
    
    context = {
        'listings': latest_listings
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
