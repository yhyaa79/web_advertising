from django import template

register = template.Library()

@register.filter(name='split_number')
def split_number(value):
    try:
        # تبدیل به عدد صحیح و فرمت کردن با کاما
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return value
