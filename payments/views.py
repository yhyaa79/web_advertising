# payments/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from listings.models import Listing
from .models import Transaction, Dispute
import uuid

@login_required
def initiate_purchase(request, listing_pk):
    listing = get_object_or_404(Listing, pk=listing_pk, status='active')
    
    if listing.seller == request.user:
        messages.error(request, 'شما نمی‌توانید آگهی خود را خریداری کنید.')
        return redirect('listings:listing_detail', pk=listing.pk)
    
    if request.method == 'POST':
        # محاسبه کمیسیون (5%)
        commission = listing.price * 0.05
        
        # ایجاد تراکنش
        transaction = Transaction.objects.create(
            buyer=request.user,
            seller=listing.seller,
            listing=listing,
            amount=listing.price,
            commission=commission,
            tracking_code=str(uuid.uuid4())[:12].upper(),
            status='pending'
        )
        
        messages.success(request, 'تراکنش ایجاد شد. لطفا پرداخت را انجام دهید.')
        return redirect('payments:payment_gateway', transaction_id=transaction.id)
    
    return render(request, 'payments/initiate_purchase.html', {'listing': listing})

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
