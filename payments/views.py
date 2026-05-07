# payments/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from listings.models import Listing
from .models import Transaction, Dispute, PriceProposal
import uuid

@login_required
def initiate_purchase(request, listing_pk):
    listing = get_object_or_404(Listing, pk=listing_pk, status='active')
    
    if listing.seller == request.user:
        messages.error(request, 'شما نمی‌توانید آگهی خود را خریداری کنید.')
        return redirect('listings:listing_detail', pk=listing.pk)
    
    # بررسی اینکه آیا قبلا پیشنهاد داده یا نه
    existing_proposal = PriceProposal.objects.filter(
        listing=listing,
        buyer=request.user
    ).first()
    
    if request.method == 'POST':
        proposed_price = request.POST.get('proposed_price')
        message = request.POST.get('message', '')
        
        try:
            proposed_price = int(proposed_price)
            
            if proposed_price <= 0:
                messages.error(request, 'قیمت پیشنهادی باید بیشتر از صفر باشد.')
                return render(request, 'payments/initiate_purchase.html', {
                    'listing': listing,
                    'existing_proposal': existing_proposal
                })
            
            if existing_proposal:
                # به‌روزرسانی پیشنهاد قبلی
                existing_proposal.proposed_price = proposed_price
                existing_proposal.message = message
                existing_proposal.status = 'pending'
                existing_proposal.save()
                messages.success(request, 'پیشنهاد قیمت شما به‌روزرسانی شد.')
            else:
                # ایجاد پیشنهاد جدید
                PriceProposal.objects.create(
                    listing=listing,
                    buyer=request.user,
                    seller=listing.seller,
                    proposed_price=proposed_price,
                    message=message
                )
                messages.success(request, 'پیشنهاد قیمت شما با موفقیت ارسال شد.')
            
            return redirect('payments:my_proposals')
            
        except (ValueError, TypeError):
            messages.error(request, 'لطفا یک قیمت معتبر وارد کنید.')
    
    context = {
        'listing': listing,
        'existing_proposal': existing_proposal
    }
    return render(request, 'payments/initiate_purchase.html', context)


@login_required
def my_proposals(request):
    """پیشنهادهای ارسال شده توسط کاربر"""
    sent_proposals = PriceProposal.objects.filter(buyer=request.user).select_related('listing', 'seller')
    received_proposals = PriceProposal.objects.filter(seller=request.user).select_related('listing', 'buyer')
    
    context = {
        'sent_proposals': sent_proposals,
        'received_proposals': received_proposals,
    }
    return render(request, 'payments/my_proposals.html', context)


@login_required
def proposal_detail(request, proposal_id):
    """جزئیات پیشنهاد قیمت"""
    proposal = get_object_or_404(PriceProposal, id=proposal_id)
    
    # بررسی دسترسی
    if proposal.buyer != request.user and proposal.seller != request.user:
        messages.error(request, 'شما به این پیشنهاد دسترسی ندارید.')
        return redirect('core:home')
    
    return render(request, 'payments/proposal_detail.html', {'proposal': proposal})


@login_required
def respond_to_proposal(request, proposal_id):
    """پاسخ فروشنده به پیشنهاد"""
    proposal = get_object_or_404(PriceProposal, id=proposal_id, seller=request.user, status='pending')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        response_message = request.POST.get('response_message', '')
        
        if action == 'accept':
            proposal.status = 'accepted'
            proposal.seller_response = response_message
            proposal.save()
            messages.success(request, 'پیشنهاد قیمت پذیرفته شد.')
        elif action == 'reject':
            proposal.status = 'rejected'
            proposal.seller_response = response_message
            proposal.save()
            messages.success(request, 'پیشنهاد قیمت رد شد.')
        
        return redirect('payments:my_proposals')
    
    return render(request, 'payments/respond_to_proposal.html', {'proposal': proposal})


@login_required
def payment_gateway(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, buyer=request.user)
    
    if request.method == 'POST':
        # شبیه‌سازی پرداخت موفق
        transaction.status = 'in_escrow'
        transaction.payment_date = timezone.now()
        transaction.save()
        
        # تغییر وضعیت آگهی
        transaction.listing.status = 'sold'
        transaction.listing.save()
        
        messages.success(request, 'پرداخت با موفقیت انجام شد. مبلغ در حساب امن نگهداری می‌شود.')
        return redirect('payments:transaction_detail', transaction_id=transaction.id)
    
    context = {
        'transaction': transaction,
        'total_amount': transaction.amount + transaction.commission,
    }
    return render(request, 'payments/payment_gateway.html', context)


@login_required
def transaction_detail(request, transaction_id):
    transaction = get_object_or_404(
        Transaction, 
        id=transaction_id,
        buyer=request.user
    ) if Transaction.objects.filter(id=transaction_id, buyer=request.user).exists() else get_object_or_404(
        Transaction,
        id=transaction_id,
        seller=request.user
    )
    
    return render(request, 'payments/transaction_detail.html', {'transaction': transaction})


@login_required
def confirm_delivery(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, buyer=request.user, status='in_escrow')
    
    if request.method == 'POST':
        transaction.status = 'completed'
        transaction.completion_date = timezone.now()
        transaction.save()
        
        messages.success(request, 'تحویل تایید شد. مبلغ به فروشنده واریز می‌شود.')
        return redirect('payments:transaction_detail', transaction_id=transaction.id)
    
    return render(request, 'payments/confirm_delivery.html', {'transaction': transaction})


@login_required
def my_transactions(request):
    purchases = Transaction.objects.filter(buyer=request.user)
    sales = Transaction.objects.filter(seller=request.user)
    
    context = {
        'purchases': purchases,
        'sales': sales,
    }
    return render(request, 'payments/my_transactions.html', context)


@login_required
def open_dispute(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    
    if transaction.buyer != request.user and transaction.seller != request.user:
        messages.error(request, 'شما مجاز به باز کردن اختلاف برای این تراکنش نیستید.')
        return redirect('core:home')
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        Dispute.objects.create(
            transaction=transaction,
            opened_by=request.user,
            reason=reason
        )
        messages.success(request, 'اختلاف شما ثبت شد و در حال بررسی است.')
        return redirect('payments:transaction_detail', transaction_id=transaction.id)
    
    return render(request, 'payments/open_dispute.html', {'transaction': transaction})
