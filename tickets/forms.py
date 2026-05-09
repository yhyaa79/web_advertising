# tickets/forms.py

from django import forms
from .models import Ticket, TicketMessage

class TicketForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'متن پیام خود را وارد کنید...'}),
        label='پیام'
    )
    
    class Meta:
        model = Ticket
        fields = ['subject', 'priority']
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'موضوع تیکت را وارد کنید...'}),
        }
        labels = {
            'subject': 'موضوع',
            'priority': 'اولویت',
        }

class TicketReplyForm(forms.ModelForm):
    class Meta:
        model = TicketMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'پاسخ خود را وارد کنید...'}),
        }
        labels = {
            'message': 'پیام',
        }
