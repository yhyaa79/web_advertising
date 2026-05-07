# notifications/context_processors.py

from .models import Notification

def unread_notifications_count(request):
    """Context processor برای نمایش تعداد اعلان‌های خوانده نشده در تمام صفحات"""
    if request.user.is_authenticated:
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return {'unread_notifications_count': count}
    return {'unread_notifications_count': 0}
