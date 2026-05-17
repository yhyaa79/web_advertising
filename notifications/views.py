# notifications/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient=request.user)
    
    # دریافت لیست اعلان‌های خوانده نشده و خوانده شده قبل از آپدیت دیتابیس
    unread_notifications = list(notifications.filter(is_read=False))
    read_notifications = list(notifications.filter(is_read=True)[:20])
    
    # علامت‌گذاری تمام اعلان‌های خوانده نشده به عنوان خوانده شده
    if unread_notifications:
        notifications.filter(is_read=False).update(is_read=True)
    
    context = {
        'unread_notifications': unread_notifications,
        'read_notifications': read_notifications,
    }
    return render(request, 'notifications/notification_list.html', context)



@login_required
def mark_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.mark_as_read()
    
    # اگر لینک عملیات دارد، به آن هدایت شود
    if notification.action_url:
        return redirect(notification.action_url)
    
    return redirect('notifications:notification_list')

@login_required
def mark_all_as_read(request):
    if request.method == 'POST':
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return redirect('notifications:notification_list')

@login_required
def delete_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    if request.method == 'POST':
        notification.delete()
    return redirect('notifications:notification_list')

@login_required
def unread_count(request):
    """API endpoint برای دریافت تعداد اعلان‌های خوانده نشده"""
    count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'count': count})
