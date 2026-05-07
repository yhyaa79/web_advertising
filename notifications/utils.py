# notifications/utils.py

from .models import Notification
from django.urls import reverse

def create_notification(recipient, notification_type, title, message, listing=None, visit_request=None, action_url=''):
    """تابع کمکی برای ایجاد اعلان"""
    return Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
        listing=listing,
        visit_request=visit_request,
        action_url=action_url
    )

def notify_visit_request(visit_request):
    """اعلان برای درخواست بازدید جدید"""
    action_url = reverse('listings:my_listings')
    create_notification(
        recipient=visit_request.listing.seller,
        notification_type='visit_request',
        title='درخواست بازدید جدید',
        message=f'{visit_request.requester.username} برای آگهی "{visit_request.listing.title}" درخواست بازدید ارسال کرده است.',
        listing=visit_request.listing,
        visit_request=visit_request,
        action_url=action_url
    )

def notify_visit_approved(visit_request):
    """اعلان برای تایید درخواست بازدید"""
    action_url = reverse('listings:listing_detail', kwargs={'pk': visit_request.listing.pk})
    create_notification(
        recipient=visit_request.requester,
        notification_type='visit_approved',
        title='درخواست بازدید تایید شد',
        message=f'درخواست بازدید شما برای آگهی "{visit_request.listing.title}" تایید شد. اکنون می‌توانید جزئیات کامل را مشاهده کنید.',
        listing=visit_request.listing,
        visit_request=visit_request,
        action_url=action_url
    )

def notify_visit_rejected(visit_request):
    """اعلان برای رد درخواست بازدید"""
    action_url = reverse('listings:listing_detail', kwargs={'pk': visit_request.listing.pk})
    create_notification(
        recipient=visit_request.requester,
        notification_type='visit_rejected',
        title='درخواست بازدید رد شد',
        message=f'متاسفانه درخواست بازدید شما برای آگهی "{visit_request.listing.title}" رد شد.',
        listing=visit_request.listing,
        visit_request=visit_request,
        action_url=action_url
    )
