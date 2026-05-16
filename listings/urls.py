# listings/urls.py

from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.listing_list, name='listing_list'),
    path('<int:pk>/', views.listing_detail, name='listing_detail'),
    path('create/', views.listing_create, name='listing_create'),
    path('<int:pk>/edit/', views.listing_edit, name='listing_edit'),
    path('<int:pk>/delete/', views.listing_delete, name='listing_delete'),
    path('<int:pk>/activate/', views.listing_activate, name='listing_activate'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('<int:pk>/request-visit/', views.request_visit, name='request_visit'),
    path('visit-request/<int:pk>/<str:action>/', views.manage_visit_request, name='manage_visit_request'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('<int:pk>/similar/', views.similar_listings, name='similar_listings'),
]
