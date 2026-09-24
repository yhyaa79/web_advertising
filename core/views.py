# core/views.py

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Sum, Avg, Q, F, Case, When, DecimalField, Min, Max
from listings.models import Listing, Category, ViewsDataPoint, IncomeDataPoint
from accounts.models import SavedListing
from django.views.generic import TemplateView 

class ComingSoonView(TemplateView):
    template_name = 'coming_soon.html'

User = get_user_model()


def get_market_insights():
    """💡 نگاهی جامع به بازار"""
    active_listings = Listing.objects.filter(status='active')
    
    # قیمت‌گذاری
    price_data = active_listings.aggregate(
        avg=Avg(Case(
            When(discount_price__isnull=False, then=F('discount_price')),
            default=F('price'),
            output_field=DecimalField()
        )),
        min=Min(Case(
            When(discount_price__isnull=False, then=F('discount_price')),
            default=F('price'),
            output_field=DecimalField()
        )),
        max=Max(Case(
            When(discount_price__isnull=False, then=F('discount_price')),
            default=F('price'),
            output_field=DecimalField()
        )),
    )
    
    return {
        'avg_price': int(price_data.get('avg') or 0),
        'min_price': int(price_data.get('min') or 0),
        'max_price': int(price_data.get('max') or 0),
        'avg_followers': int(active_listings.aggregate(Avg('followers_count'))['followers_count__avg'] or 0),
        'avg_monthly_income': int(active_listings.aggregate(Avg('monthly_income'))['monthly_income__avg'] or 0),
        'avg_views': int(active_listings.aggregate(Avg('most_view'))['most_view__avg'] or 0),
    }


def get_platform_stats():
    """📊 آمارهای کلی پلتفرم"""
    now = timezone.now()
    today = now.date()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    
    # شمارش کاربران
    total_users = User.objects.count()
    new_users_today = User.objects.filter(
        date_joined__date=today
    ).count()
    new_users_week = User.objects.filter(
        date_joined__gte=week_ago
    ).count()
    
    # شمارش آگهی‌ها
    active_listings = Listing.objects.filter(status='active').count()
    new_listings_today = Listing.objects.filter(
        status='active',
        created_at__date=today
    ).count()
    new_listings_week = Listing.objects.filter(
        status='active',
        created_at__gte=week_ago
    ).count()
    sold_listings = Listing.objects.filter(status='sold').count()
    
    # آگهی‌های تایید‌شده
    verified_listings = Listing.objects.filter(
        status='active',
        is_verified=True
    ).count()
    
    # آگهی‌های درآمدزا
    income_listings = Listing.objects.filter(
        status='active',
        is_income=True,
        monthly_income__gt=0
    ).count()
    
    return {
        'total_users': total_users,
        'new_users_today': new_users_today,
        'new_users_week': new_users_week,
        'active_listings': active_listings,
        'new_listings_today': new_listings_today,
        'new_listings_week': new_listings_week,
        'sold_listings': sold_listings,
        'verified_listings': verified_listings,
        'income_listings': income_listings,
    }


def get_views_statistics():
    """👁️ آمارهای بازدید"""
    now = timezone.now()
    today = now.date()
    week_ago = (now - timedelta(days=7)).date()
    month_ago = (now - timedelta(days=30)).date()

    # بازدیدهای امروز
    today_views = ViewsDataPoint.objects.filter(
        listing__status='active',
        date=today
    ).aggregate(total=Sum('views'))['total'] or 0

    # بازدیدهای هفته
    week_views = ViewsDataPoint.objects.filter(
        listing__status='active',
        date__gte=week_ago
    ).aggregate(total=Sum('views'))['total'] or 0

    # بازدیدهای ماه
    month_views = ViewsDataPoint.objects.filter(
        listing__status='active',
        date__gte=month_ago
    ).aggregate(total=Sum('views'))['total'] or 0

    # بازدیدهای کل (از روی فیلد شمارنده خود Listing)
    total_views = Listing.objects.filter(
        status='active'
    ).aggregate(Sum('views_count'))['views_count__sum'] or 0

    return {
        'today': today_views,
        'week': week_views,
        'month': month_views,
        'total': total_views,
    }


def get_top_categories():
    """🔥 حوزه‌های پرطرفدار"""
    # گروه‌بندی آگهی‌های فعال بر اساس اسلاگ دسته‌بندی
    rows = (
        Listing.objects
        .filter(status='active', category__isnull=False)
        .exclude(category='')
        .values('category')
        .annotate(
            count=Count('id'),
            avg_price=Avg(Case(
                When(discount_price__isnull=False, then=F('discount_price')),
                default=F('price'),
                output_field=DecimalField()
            )),
        )
        .order_by('-count')[:6]
    )

    # دیکشنری اسلاگ ← نام فارسی (زیردسته)
    platform_labels = dict(Category.PLATFORM_CHOICES)

    # دیکشنری اسلاگ ← نام فارسی (دسته‌ی کلی) به‌عنوان fallback
    main_labels = {slug: label for slug, label, _ in Category.PLATFORM_CATEGORIES}

    result = []
    for row in rows:
        slug = row['category']
        name = platform_labels.get(slug) or main_labels.get(slug) or slug
        result.append({
            'name': name,
            'slug': slug,
            'count': row['count'],
            'avg_price': int(row['avg_price'] or 0),
        })
    return result



def get_trending_listings():
    """🚀 آگهی‌های روند"""
    today = timezone.now().date()

    trending = Listing.objects.filter(
        status='active',
        views_data_points__date=today
    ).annotate(
        today_views=Sum('views_data_points__views')
    ).order_by('-today_views')[:4]

    return trending


def get_special_listings():
    """✨ آگهی‌های ویژه"""
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    
    # تازه‌ترین‌ها (این هفته)
    latest = Listing.objects.filter(
        status='active',
        created_at__gte=week_ago
    ).order_by('-created_at')[:4]
    
    # تخفیف‌دار‌ها
    discounted = Listing.objects.filter(
        status='active',
        discount_price__isnull=False
    ).exclude(discount_price=0).order_by('-created_at')[:4]
    
    # پرباز‌دید‌ترین‌ها (این ماه)
    month_ago = now - timedelta(days=30)
    most_viewed = Listing.objects.filter(
        status='active',
        created_at__gte=month_ago
    ).order_by('-most_view')[:4]
    
    # بیشترین دنبال‌کننده
    most_followers = Listing.objects.filter(
        status='active'
    ).order_by('-followers_count')[:4]
    
    # بیشترین درآمد
    highest_income = Listing.objects.filter(
        status='active',
        is_income=True,
        monthly_income__gt=0
    ).order_by('-monthly_income')[:4]
    
    return {
        'latest': latest,
        'discounted': discounted,
        'most_viewed': most_viewed,
        'most_followers': most_followers,
        'highest_income': highest_income,
    }


def get_market_opportunities():
    """💎 فرصت‌های بازار"""
    # بیشترین افزایش بازدید
    trending = Listing.objects.filter(
        status='active',
        views_count__gt=0
    ).order_by('-views_count')[:3]
    
    # تخفیف‌های بیشتر از ۲۰٪
    big_discounts = []
    for listing in Listing.objects.filter(
        status='active',
        discount_price__isnull=False
    ).order_by('-created_at')[:10]:
        if listing.price and listing.discount_price:
            discount_pct = ((listing.price - listing.discount_price) / listing.price) * 100
            if discount_pct >= 20:
                big_discounts.append({
                    'listing': listing,
                    'discount_pct': int(discount_pct),
                })
    
    return {
        'trending': trending,
        'big_discounts': big_discounts[:3],
    }


def format_number(num):
    """فرمت‌کردن اعداد بزرگ به K یا M"""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(int(num))


def home(request):
    """صفحه اصلی با داده‌های دینامیک جامع"""
    
    # جمع‌آوری تمام داده‌ها
    platform_stats = get_platform_stats()
    market_insights = get_market_insights()
    views_stats = get_views_statistics()
    top_categories = get_top_categories()
    special_listings = get_special_listings()
    market_opportunities = get_market_opportunities()
    trending_listings = get_trending_listings()
    
    # اگر کاربر لاگین است، آگهی‌های ذخیره‌شده را بگیر
    saved_listing_ids = []
    if request.user.is_authenticated:
        saved_listing_ids = list(
            SavedListing.objects.filter(user=request.user).values_list('listing_id', flat=True)
        )
    
    context = {
        # آمار پلتفرم
        'platform_stats': platform_stats,
        
        # بازار
        'market_insights': market_insights,
        
        # بازدیدها
        'views_stats': views_stats,
        
        # دسته‌بندی‌ها
        'top_categories': top_categories,
        
        # آگهی‌های ویژه
        'latest_listings': special_listings['latest'],
        'discounted_listings': special_listings['discounted'],
        'most_viewed_listings': special_listings['most_viewed'],
        'most_followers_listings': special_listings['most_followers'],
        'highest_income_listings': special_listings['highest_income'],
        
        # فرصت‌ها
        'market_opportunities': market_opportunities,
        'trending_listings': trending_listings,
        
        # ذخیره‌شده‌ها
        'saved_listing_ids': saved_listing_ids,
        
        # توابع کمکی
        'format_number': format_number,
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
        listings = active_listings.filter(boost=True).order_by('-created_at')[offset:offset+limit]
    elif list_type == 'verified':
        listings = active_listings.filter(is_verified=True).order_by('-created_at')[offset:offset+limit]
    elif list_type == 'highest_income':
        listings = active_listings.filter(
            monthly_income__isnull=False
        ).order_by('-monthly_income')[offset:offset+limit]
    else:
        listings = []
    
    return render(request, 'core/partials/listing_cards.html', {'listings': listings})