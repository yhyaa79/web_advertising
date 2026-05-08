# tickets/forms.py


from django import forms
from .models import Ticket, TicketMessage, TicketCategory


class TicketCreateForm(forms.ModelForm):
    """فرم ایجاد تیکت جدید"""
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'متن پیام خود را بنویسید...'
        }),
        label='پیام'
    )
    attachment = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label='فایل پیوست (اختیاری)'
    )

    class Meta:
        model = Ticket
        fields = ['category', 'subject', 'priority']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'موضوع تیکت را وارد کنید'
            }),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = TicketCategory.objects.filter(is_active=True)


class TicketReplyForm(forms.ModelForm):
    """فرم پاسخ به تیکت"""
    class Meta:
        model = TicketMessage
        fields = ['message', 'attachment']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'پاسخ خود را بنویسید...'
            }),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'message': 'پیام',
            'attachment': 'فایل پیوست (اختیاری)',
        }


class TicketFilterForm(forms.Form):
    """فرم فیلتر تیکت‌ها"""
    status = forms.ChoiceField(
        choices=[('', 'همه')] + list(Ticket._meta.get_field('status').choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='وضعیت'
    )
    category = forms.ModelChoiceField(
        queryset=TicketCategory.objects.filter(is_active=True),
        required=False,
        empty_label='همه دسته‌ها',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='دسته‌بندی'
    )
    priority = forms.ChoiceField(
        choices=[('', 'همه')] + list(Ticket._meta.get_field('priority').choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='اولویت'
    )
