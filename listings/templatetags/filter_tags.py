# listings/templatetags/filter_tags.py


from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def filter_url(context, **kwargs):
    """ساخت URL با حفظ فیلترهای فعلی + override کردن کلیدهای داده‌شده"""
    request = context['request']
    query = request.GET.copy()

    for key, value in kwargs.items():
        if value:
            query[key] = value
        else:
            query.pop(key, None)

    # اگر main_activity عوض شد ولی areas_activity قبلی مانده، پاکش کن
    if 'main_activity' in kwargs and 'areas_activity' not in kwargs:
        query.pop('areas_activity', None)

    return '?' + query.urlencode()