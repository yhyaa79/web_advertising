from django import template
from django.utils import timezone
from datetime import timedelta
import jdatetime

register = template.Library()


@register.filter
def time_ago(value):
    if not value:
        return ""

    now = timezone.now()

    # اگر datetime ناآگاه بود، آگاهش می‌کنیم
    if timezone.is_naive(value):
        value = timezone.make_aware(value, timezone.get_current_timezone())

    diff = now - value

    if diff < timedelta(minutes=1):
        seconds = int(diff.total_seconds())
        return f"{seconds} ثانیه قبل" if seconds > 0 else "لحظاتی قبل"
    elif diff < timedelta(hours=1):
        minutes = diff.seconds // 60
        return f"{minutes} دقیقه قبل"
    elif diff < timedelta(days=1):
        hours = diff.seconds // 3600
        return f"{hours} ساعت قبل"
    elif diff < timedelta(weeks=1):
        days = diff.days
        return f"{days} روز قبل"
    elif diff < timedelta(days=30):
        weeks = diff.days // 7
        return f"{weeks} هفته قبل"
    elif diff < timedelta(days=365):
        months = diff.days // 30
        return f"{months} ماه قبل"
    else:
        years = diff.days // 365
        return f"{years} سال قبل"


@register.filter
def jalali_date(value):
    if not value:
        return ""

    # تبدیل به تاریخ شمسی
    j_date = jdatetime.datetime.fromgregorian(datetime=value)

    month_names = {
        1: "فروردین",
        2: "اردیبهشت",
        3: "خرداد",
        4: "تیر",
        5: "مرداد",
        6: "شهریور",
        7: "مهر",
        8: "آبان",
        9: "آذر",
        10: "دی",
        11: "بهمن",
        12: "اسفند",
    }

    return f"{j_date.day} {month_names[j_date.month]} {j_date.year}"
