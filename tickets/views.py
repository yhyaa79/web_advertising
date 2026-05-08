# tickets/views.py


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Max
from .models import Ticket, TicketMessage, TicketCategory, TicketStatus
from .forms import TicketCreateForm, TicketReplyForm, TicketFilterForm


@login_required
def ticket_list(request):
    """لیست تیکت‌های کاربر"""
    tickets = Ticket.objects.filter(user=request.user).annotate(
        message_count=Count('messages'),
        last_update=Max('messages__created_at')
    ).select_related('category')

    # فیلتر کردن
    filter_form = TicketFilterForm(request.GET)
    if filter_form.is_valid():
        status = filter_form.cleaned_data.get('status')
        category = filter_form.cleaned_data.get('category')
        priority = filter_form.cleaned_data.get('priority')

        if status:
            tickets = tickets.filter(status=status)
        if category:
            tickets = tickets.filter(category=category)
        if priority:
            tickets = tickets.filter(priority=priority)

    # جستجو
    search_query = request.GET.get('search', '')
    if search_query:
        tickets = tickets.filter(
            Q(subject__icontains=search_query) |
            Q(messages__message__icontains=search_query)
        ).distinct()

    # صفحه‌بندی
    paginator = Paginator(tickets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
        'search_query': search_query,
    }
    return render(request, 'tickets/ticket_list.html', context)


@login_required
def ticket_create(request):
    """ایجاد تیکت جدید"""
    if request.method == 'POST':
        form = TicketCreateForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            # ایجاد اولین پیام
            TicketMessage.objects.create(
                ticket=ticket,
                sender=request.user,
                message=form.cleaned_data['message'],
                attachment=form.cleaned_data.get('attachment')
            )

            messages.success(request, 'تیکت شما با موفقیت ثبت شد.')
            return redirect('tickets:ticket_detail', pk=ticket.pk)
    else:
        form = TicketCreateForm()

    context = {'form': form}
    return render(request, 'tickets/ticket_create.html', context)


@login_required
def ticket_detail(request, pk):
    """جزئیات و پاسخ به تیکت"""
    ticket = get_object_or_404(Ticket, pk=pk, user=request.user)
    ticket_messages = ticket.messages.select_related('sender').order_by('created_at')

    if request.method == 'POST':
        if ticket.is_closed:
            messages.warning(request, 'این تیکت بسته شده است. ابتدا آن را بازگشایی کنید.')
            return redirect('tickets:ticket_detail', pk=pk)

        form = TicketReplyForm(request.POST, request.FILES)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.ticket = ticket
            reply.sender = request.user
            reply.save()

            # تغییر وضعیت تیکت به "باز" اگر در انتظار پاسخ کاربر بود
            if ticket.status == TicketStatus.WAITING_USER:
                ticket.status = TicketStatus.OPEN
                ticket.save()

            messages.success(request, 'پاسخ شما ثبت شد.')
            return redirect('tickets:ticket_detail', pk=pk)
    else:
        form = TicketReplyForm()

    context = {
        'ticket': ticket,
        'messages': ticket_messages,
        'form': form,
    }
    return render(request, 'tickets/ticket_detail.html', context)


@login_required
def ticket_close(request, pk):
    """بستن تیکت"""
    ticket = get_object_or_404(Ticket, pk=pk, user=request.user)
    
    if request.method == 'POST':
        ticket.close()
        messages.success(request, 'تیکت با موفقیت بسته شد.')
        return redirect('tickets:ticket_detail', pk=pk)
    
    return redirect('tickets:ticket_detail', pk=pk)


@login_required
def ticket_reopen(request, pk):
    """بازگشایی تیکت"""
    ticket = get_object_or_404(Ticket, pk=pk, user=request.user)
    
    if request.method == 'POST':
        ticket.reopen()
        messages.success(request, 'تیکت مجدداً بازگشایی شد.')
        return redirect('tickets:ticket_detail', pk=pk)
    
    return redirect('tickets:ticket_detail', pk=pk)
