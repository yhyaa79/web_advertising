# accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),

    # آگهی‌های ذخیره شده
    path('saved-listings/', views.saved_listings_view, name='saved_listings'),
    path('toggle-save-listing/<int:listing_id>/', views.toggle_save_listing, name='toggle_save_listing'),
    
    # یادداشت‌ها
    path('listing-note/<int:listing_id>/', views.save_listing_note, name='save_listing_note'),
    path('delete-listing-note/<int:listing_id>/', views.delete_listing_note, name='delete_listing_note'),
]
