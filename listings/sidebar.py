# listings/sidebar.py
from django.db.models import Avg, Min, Max, Count, Sum


def build_sidebar_context(request, base_qs, activity_categories=()):
    """
    base_qs: کوئری‌ست آگهی‌های فعال «بعد از اعمال فیلترها و قبل از صفحه‌بندی»
    خروجی: دیکشنری که با کلید 'sidebar' به تمپلیت داده می‌شود.
    هر بخش در try جدا است تا خطا در یکی، کل صفحه را خراب نکند.
    """
    from .models import Listing, VisitRequest          # ⚠️ نام مدل‌ها را چک کن
    data = {}

    # ─── داده‌های عمومی (برای همه کاربران) ───
    try:
        data['market'] = base_qs.aggregate(
            avg_price=Avg('price'), min_price=Min('price'), max_price=Max('price'),
            avg_followers=Avg('followers_count'), avg_income=Avg('monthly_income'),
        )
        data['verified_count'] = base_qs.filter(is_verified=True).count()
        data['income_count'] = base_qs.filter(monthly_income__gt=0).count()
        data['newest'] = base_qs.order_by('-created_at')[:4]
        data['most_viewed'] = base_qs.order_by('-views_count')[:4]
        data['discounted'] = (base_qs.filter(discount_price__isnull=False)
                              .exclude(discount_price=0)[:4])
    except Exception:
        pass

    # ─── پرطرفدارترین حوزه‌ها با تعداد آگهی ───
    try:
        labels = {s: l for _, _, subs in activity_categories for s, l in subs}
        rows = (base_qs.exclude(areas_activity='')
                .values('areas_activity').annotate(c=Count('id')).order_by('-c')[:6])
        data['top_activities'] = [
            {'slug': r['areas_activity'],
             'label': labels.get(r['areas_activity'], r['areas_activity']),
             'count': r['c']} for r in rows
        ]
    except Exception:
        pass

    # ─── داده‌های شخصی (فقط کاربر لاگین‌شده) ───
    user = request.user
    if user.is_authenticated:

        # سطح احراز هویت (ساده). اگر تابع kyc خودت را داری، اینجا جایگزینش کن.
        try:
            profile = getattr(user, 'profile', None)   # ⚠️ related_name پروفایل
            checks = [
                bool(user.phone_number), bool(user.national_code),
                bool(user.profile_image), bool(getattr(user, 'is_verified', False)),
                bool(getattr(profile, 'address', '')), bool(getattr(profile, 'city', '')),
                bool(getattr(profile, 'iban_number', '')),
            ]
            data['kyc_level'] = int(sum(checks) / len(checks) * 100)
        except Exception:
            data['kyc_level'] = 0

        # اعلان‌های خوانده‌نشده
        try:
            from notifications.models import Notification
            unread = Notification.objects.filter(recipient=user, is_read=False)   # ← recipient
            data['unread_count'] = unread.count()
            data['notifications'] = unread.order_by('-created_at')[:3]
        except Exception:
            pass

        # درخواست‌های بازدید در انتظارِ آگهی‌های من
        try:
            pending = (VisitRequest.objects
                       .filter(listing__seller=user, status='pending')   # ⚠️ status
                       .select_related('requester', 'listing'))
            data['pending_count'] = pending.count()
            data['pending_requests'] = pending.order_by('-created_at')[:3]
        except Exception:
            pass

        # خلاصه آگهی‌های من
        try:
            mine = Listing.objects.filter(seller=user)
            data['my_stats'] = {
                'total': mine.count(),
                'active': mine.filter(status='active').count(),
                'pending': mine.filter(status='pending').count(),
                'rejected': mine.filter(status='rejected').count(),
                'views': mine.aggregate(v=Sum('views_count'))['v'] or 0,
            }
        except Exception:
            pass

    return data