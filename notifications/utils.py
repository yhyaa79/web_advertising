# notifications/utils.py

from .models import Notification
from django.urls import reverse


# notifications/utils.py
from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(recipient, notification_type, title, message, related_object=None):
    """
    تابع کمکی برای ایجاد اعلان
    """
    notification = Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message
    )
    
    if related_object:
        notification.content_type = ContentType.objects.get_for_model(related_object)
        notification.object_id = related_object.pk
        notification.save()
    
    return notification



def notify_visit_request(visit_request):
    """اعلان برای درخواست بازدید جدید"""
    create_notification(
        recipient=visit_request.listing.seller,
        notification_type='visit_request',
        title='درخواست بازدید جدید',
        message=f'{visit_request.requester.username} برای آگهی "{visit_request.listing.title}" درخواست بازدید ارسال کرده است.',
        related_object=visit_request
    )

def notify_visit_approved(visit_request):
    """اعلان برای تایید درخواست بازدید"""
    create_notification(
        recipient=visit_request.requester,
        notification_type='visit_approved',
        title='درخواست بازدید تایید شد',
        message=f'درخواست بازدید شما برای آگهی "{visit_request.listing.title}" تایید شد. اکنون می‌توانید جزئیات کامل را مشاهده کنید.',
        related_object=visit_request
    )

def notify_visit_rejected(visit_request):
    """اعلان برای رد درخواست بازدید"""
    create_notification(
        recipient=visit_request.requester,
        notification_type='visit_rejected',
        title='درخواست بازدید رد شد',
        message=f'متاسفانه درخواست بازدید شما برای آگهی "{visit_request.listing.title}" رد شد.',
        related_object=visit_request
    )















def notify_new_proposal(proposal):
    """
    اعلان برای فروشنده هنگام دریافت پیشنهاد قیمت جدید
    """
    return create_notification(
        recipient=proposal.seller,
        notification_type='proposal',
        title='پیشنهاد قیمت جدید',
        message=f'{proposal.buyer.username} برای آگهی "{proposal.listing.title}" پیشنهاد قیمت داده است.',
        related_object=proposal
    )


def notify_proposal_accepted(proposal):
    """
    اعلان برای خریدار هنگام پذیرش پیشنهاد
    """
    return create_notification(
        recipient=proposal.buyer,
        notification_type='proposal',
        title='پیشنهاد شما پذیرفته شد',
        message=f'فروشنده پیشنهاد شما برای آگهی "{proposal.listing.title}" را پذیرفت.',
        related_object=proposal
    )


def notify_proposal_rejected(proposal):
    """
    اعلان برای خریدار هنگام رد پیشنهاد
    """
    return create_notification(
        recipient=proposal.buyer,
        notification_type='proposal',
        title='پیشنهاد شما رد شد',
        message=f'متاسفانه فروشنده پیشنهاد شما برای آگهی "{proposal.listing.title}" را رد کرد.',
        related_object=proposal
    )




