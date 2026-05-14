# tickets/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket, TicketMessage
from .forms import TicketForm, TicketReplyForm

@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})


@login_required
def ticket_create(request):

    initial_data = {
        'subject': request.GET.get('subject', ''),
        'category': request.GET.get('category', ''),
    }

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            message_text = form.cleaned_data['message']
            attachment = form.cleaned_data.get('attachment')

            TicketMessage.objects.create(
                ticket=ticket,
                sender=request.user,
                message=message_text,
                attachment=attachment,
                is_admin_reply=False
            )

            messages.success(request, 'تیکت شما با موفقیت ثبت شد.')
            return redirect('tickets:ticket_detail', pk=ticket.pk)

    else:
        form = TicketForm(initial=initial_data)

    return render(request, 'tickets/ticket_create.html', {'form': form})


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk, user=request.user)
    ticket_messages = ticket.messages.all().order_by('created_at')
    
    # بررسی اینکه آیا کاربر می‌تواند پاسخ دهد
    can_reply = ticket.status != 'closed' and ticket.has_admin_reply()
    
    if request.method == 'POST' and can_reply:
        form = TicketReplyForm(request.POST, request.FILES)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.ticket = ticket
            reply.sender = request.user
            reply.is_admin_reply = False
            reply.save()
            
            # تغییر وضعیت تیکت به باز
            ticket.status = 'open'
            ticket.save()
            
            messages.success(request, 'پاسخ شما ارسال شد.')
            return redirect('tickets:ticket_detail', pk=ticket.pk)
    else:
        form = TicketReplyForm()
    
    context = {
        'ticket': ticket,
        'ticket_messages': ticket_messages,
        'form': form,
        'can_reply': can_reply,
    }
    return render(request, 'tickets/ticket_detail.html', context)

@login_required
def ticket_close(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk, user=request.user)
    if ticket.status != 'closed':
        ticket.status = 'closed'
        ticket.save()
        messages.success(request, 'تیکت بسته شد.')
    return redirect('tickets:ticket_detail', pk=ticket.pk)
