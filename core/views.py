# core/views.py

from django.shortcuts import render
from listings.models import Listing, Category

def home(request):
    latest_listings = Listing.objects.filter(status='active')[:6]
    categories = Category.objects.all()
    
    context = {
        'latest_listings': latest_listings,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')
