# listings/admin.py
from django.contrib import admin
from .models import Category, Listing, IncomeProof, ListingImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'platform']
    list_filter = ['platform']

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'category', 'price', 'status', 'created_at']
    list_filter = ['status', 'category']
