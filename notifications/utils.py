
# notifications/utils.py
from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(recipient, notification_type, title, message, related_object=None, action_url=None):
    """
    تابع کمکی برای ایجاد اعلان
    """
    notification = Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message
    )
    
    # ذخیره related_object در صورت وجود
    if related_object:
        from django.contrib.contenttypes.models import ContentType
        notification.content_type = ContentType.objects.get_for_model(related_object)
        notification.object_id = related_object.pk
        
    # ذخیره action_url در صورت وجود
    if action_url:
        notification.action_url = action_url
        
    notification.save()
    
    return notification

