# listings/urls.py

from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.listing_list, name='listing_list'),
    path('<int:pk>/', views.listing_detail, name='listing_detail'),
    path('create/', views.listing_create, name='listing_create'),
    path('<int:pk>/edit/', views.listing_edit, name='listing_edit'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('<int:listing_pk>/add-proof/', views.add_income_proof, name='add_income_proof'),
]
