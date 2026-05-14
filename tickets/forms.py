# tickets/forms.py

from django import forms
from .models import Ticket, TicketMessage

class TicketForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'متن پیام خود را وارد کنید...'}),
        label='پیام'
    )

    attachment = forms.FileField(
        required=False,
        label='فایل پیوست'
    )
    
    class Meta:
        model = Ticket
        fields = ['subject', 'category', 'priority']   # category اضافه شد
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'موضوع تیکت را وارد کنید...'}),
        }
        labels = {
            'subject': 'موضوع',
            'category': 'دسته‌بندی',
            'priority': 'اولویت',
        }


class TicketReplyForm(forms.ModelForm):

    attachment = forms.FileField(
        required=False,
        label='فایل پیوست'
    )

    class Meta:
        model = TicketMessage
        fields = ['message', 'attachment']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'پاسخ خود را وارد کنید...'}),
        }
        labels = {
            'message': 'پیام',
            'attachment': 'فایل پیوست',
        }
