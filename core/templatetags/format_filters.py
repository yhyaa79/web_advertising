# core/templatetags/format_filters.py
from django import template

register = template.Library()

PERSIAN_DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')


def _to_persian(s):
    return str(s).translate(PERSIAN_DIGITS)


@register.filter(name='format_number')
def format_number(value):
    """
    نمایش اعداد بزرگ به‌صورت خلاصه با ارقام فارسی.
    ۱۲۳۴۵ → ۱۲.۳K
    ۱۲۳۴۵۶۷ → ۱.۲M
    ۱۲۳۴۵۶۷۸۹ → ۱.۲B
    زیر هزار: با جداکننده هزارگان
    """
    if value is None or value == '':
        return '—'

    try:
        num = float(value)
    except (ValueError, TypeError):
        return value

    sign = '-' if num < 0 else ''
    num = abs(num)

    if num >= 1_000_000_000:
        short = f"{num / 1_000_000_000:.1f}".rstrip('0').rstrip('.') + 'B'
    elif num >= 1_000_000:
        short = f"{num / 1_000_000:.1f}".rstrip('0').rstrip('.') + 'M'
    elif num >= 1_000:
        short = f"{num / 1_000:.1f}".rstrip('0').rstrip('.') + 'K'
    else:
        return sign + _to_persian(f"{int(num):,}")

    # اعداد لاتین را فارسی کن، اما حرف واحد را نگه دار
    return sign + short.translate(PERSIAN_DIGITS)