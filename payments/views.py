# payments/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from listings.models import Listing
from .models import Transaction, Dispute, PriceProposal, ChatRoom, ChatMessage
import uuid
from django.db import models
from notifications.utils import notify_new_proposal, notify_proposal_accepted, notify_proposal_rejected



@login_required
def initiate_purchase(request, listing_pk):
    listing = get_object_or_404(Listing, pk=listing_pk, status='active')
    
    if listing.seller == request.user:
        messages.error(request, 'شما نمی‌توانید آگهی خود را خریداری کنید.')
        return redirect('listings:listing_detail', pk=listing.pk)
    
    existing_proposal = PriceProposal.objects.filter(
        listing=listing,
        buyer=request.user
    ).first()
    
    if request.method == 'POST':
        send_custom_price = request.POST.get('send_custom_price')
        
        if send_custom_price:
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
                
            except (ValueError, TypeError):
                messages.error(request, 'لطفا یک قیمت معتبر وارد کنید.')
                return render(request, 'payments/initiate_purchase.html', {
                    'listing': listing,
                    'existing_proposal': existing_proposal
                })
        else:
            proposed_price = listing.price
            message = ''
        
        if existing_proposal:
            existing_proposal.proposed_price = proposed_price
            existing_proposal.message = message
            existing_proposal.status = 'negotiating'  # تغییر از pending به negotiating
            existing_proposal.save()
            
            # ایجاد یا دریافت اتاق چت
            ChatRoom.objects.get_or_create(
                proposal=existing_proposal,
                defaults={
                    'buyer': existing_proposal.buyer,
                    'seller': existing_proposal.seller,
                    'listing': existing_proposal.listing
                }
            )
            
            notify_new_proposal(existing_proposal)
            
            messages.success(request, 'پیشنهاد قیمت شما به‌روزرسانی شد و می‌توانید با فروشنده چت کنید.')
        else:
            new_proposal = PriceProposal.objects.create(
                listing=listing,
                buyer=request.user,
                seller=listing.seller,
                proposed_price=proposed_price,
                message=message,
                status='negotiating'  # مستقیم negotiating به جای pending
            )
            
            # ایجاد اتاق چت
            ChatRoom.objects.get_or_create(
                proposal=new_proposal,
                defaults={
                    'buyer': new_proposal.buyer,
                    'seller': new_proposal.seller,
                    'listing': new_proposal.listing
                }
            )
            
            notify_new_proposal(new_proposal)
            
            messages.success(request, 'پیشنهاد قیمت شما با موفقیت ارسال شد و می‌توانید با فروشنده چت کنید.')
        
        return redirect('payments:my_transactions')
    
    context = {
        'listing': listing,
        'existing_proposal': existing_proposal
    }
    return render(request, 'payments/initiate_purchase.html', context)



@login_required
def respond_to_proposal(request, proposal_id):
    """پاسخ فروشنده به پیشنهاد"""
    proposal = get_object_or_404(PriceProposal, id=proposal_id, seller=request.user, status='pending')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        response_message = request.POST.get('response_message', '')
        
        if action == 'accept':
            proposal.status = 'negotiating'
            proposal.seller_response = response_message
            proposal.save()
            
            # ایجاد اتاق چت
            ChatRoom.objects.get_or_create(
                proposal=proposal,
                defaults={
                    'buyer': proposal.buyer,
                    'seller': proposal.seller,
                    'listing': proposal.listing
                }
            )
            
            notify_proposal_accepted(proposal)
            
            messages.success(request, 'پیشنهاد قیمت پذیرفته شد.')
            
        elif action == 'reject':
            proposal.status = 'rejected'
            proposal.seller_response = response_message
            proposal.save()
            
            notify_proposal_rejected(proposal)
            
            messages.success(request, 'پیشنهاد قیمت رد شد.')
        
        return redirect('payments:my_transactions')
    
    return render(request, 'payments/respond_to_proposal.html', {'proposal': proposal})


@login_required
def proposal_detail(request, proposal_id):
    """جزئیات پیشنهاد قیمت"""
    proposal = get_object_or_404(PriceProposal, id=proposal_id)
    
    if proposal.buyer != request.user and proposal.seller != request.user:
        messages.error(request, 'شما به این پیشنهاد دسترسی ندارید.')
        return redirect('core:home')
    
    return render(request, 'payments/proposal_detail.html', {'proposal': proposal})


@login_required
@require_POST
def agree_to_deal(request, proposal_id):
    """موافقت با معامله"""
    proposal = get_object_or_404(PriceProposal, id=proposal_id)
    
    if proposal.buyer != request.user and proposal.seller != request.user:
        return JsonResponse({'error': 'دسترسی غیرمجاز'}, status=403)
    
    # بررسی وضعیت
    if proposal.status not in ['negotiating', 'accepted']:
        return JsonResponse({'error': 'این پیشنهاد قابل تایید نیست'}, status=400)
    
    # ثبت موافقت کاربر
    if request.user == proposal.buyer:
        proposal.buyer_agreed = True
    elif request.user == proposal.seller:
        proposal.seller_agreed = True
    
    # اگر هر دو موافقت کردند
    if proposal.buyer_agreed and proposal.seller_agreed:
        proposal.status = 'deal_confirmed'
        
        # ایجاد تراکنش
        tracking_code = str(uuid.uuid4())[:8].upper()
        transaction = Transaction.objects.create(
            buyer=proposal.buyer,
            seller=proposal.seller,
            listing=proposal.listing,
            amount=proposal.proposed_price,
            commission=0,  # بدون کمیسیون
            tracking_code=tracking_code,
            status='sold'
        )
        
        # تغییر وضعیت آگهی
        proposal.listing.status = 'sold'
        proposal.listing.save()
        
        proposal.save()
        
        return JsonResponse({
            'success': True,
            'message': 'معامله تایید شد! تراکنش ایجاد گردید.',
            'status': 'deal_confirmed',
            'buyer_agreed': proposal.buyer_agreed,
            'seller_agreed': proposal.seller_agreed
        })
    else:
        proposal.save()
        return JsonResponse({
            'success': True,
            'message': 'موافقت شما ثبت شد. منتظر تایید طرف مقابل هستیم.',
            'status': proposal.status,
            'buyer_agreed': proposal.buyer_agreed,
            'seller_agreed': proposal.seller_agreed
        })


@login_required
@require_POST
def cancel_deal(request, proposal_id):
    """کنسل کردن معامله"""
    proposal = get_object_or_404(PriceProposal, id=proposal_id)
    
    if proposal.buyer != request.user and proposal.seller != request.user:
        return JsonResponse({'error': 'دسترسی غیرمجاز'}, status=403)
    
    # بررسی وضعیت
    if proposal.status not in ['negotiating', 'accepted']:
        return JsonResponse({'error': 'این پیشنهاد قابل کنسل نیست'}, status=400)
    
    # ثبت کنسل
    if request.user == proposal.buyer:
        proposal.buyer_cancelled = True
    elif request.user == proposal.seller:
        proposal.seller_cancelled = True
    
    proposal.status = 'deal_cancelled'
    proposal.save()
    
    return JsonResponse({
        'success': True,
        'message': 'معامله کنسل شد.',
        'status': 'deal_cancelled'
    })


@login_required
def payment_gateway(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, buyer=request.user)
    
    if request.method == 'POST':
        transaction.status = 'in_escrow'
        transaction.payment_date = timezone.now()
        transaction.save()
        
        transaction.listing.status = 'sold'
        transaction.listing.save()
        
        messages.success(request, 'پرداخت با موفقیت انجام شد. مبلغ در حساب امن نگهداری می‌شود.')
        return redirect('payments:transaction_detail', transaction_id=transaction.id)
    
    context = {
        'transaction': transaction,
        'total_amount': transaction.amount,  # فقط مبلغ اصلی، بدون کمیسیون
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
    purchases = Transaction.objects.filter(buyer=request.user).select_related('listing', 'seller').order_by('-created_at')
    sales = Transaction.objects.filter(seller=request.user).select_related('listing', 'buyer').order_by('-created_at')
    
    sent_proposals = PriceProposal.objects.filter(
        buyer=request.user
    ).select_related('listing', 'seller').order_by('-created_at')
    
    received_proposals = PriceProposal.objects.filter(
        seller=request.user
    ).select_related('listing', 'buyer').order_by('-created_at')
    
    # پیشنهادات تایید شده
    accepted_proposals = PriceProposal.objects.filter(
        status__in=['negotiating', 'accepted', 'deal_confirmed', 'deal_cancelled']
    ).filter(
        models.Q(buyer=request.user) | models.Q(seller=request.user)
    ).select_related('listing', 'buyer', 'seller').order_by('-updated_at')
    
    context = {
        'purchases': purchases,
        'sales': sales,
        'sent_proposals': sent_proposals,
        'received_proposals': received_proposals,
        'accepted_proposals': accepted_proposals,
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


# ========== ویوهای چت ==========

@login_required
def chat_view(request, proposal_id):
    """نمایش صفحه چت"""
    proposal = get_object_or_404(PriceProposal, id=proposal_id)
    
    # بررسی دسترسی
    if proposal.buyer != request.user and proposal.seller != request.user:
        messages.error(request, 'شما به این چت دسترسی ندارید.')
        return redirect('payments:my_transactions')
    
    # ایجاد یا دریافت اتاق چت
    chat_room, created = ChatRoom.objects.get_or_create(
        proposal=proposal,
        defaults={
            'buyer': proposal.buyer,
            'seller': proposal.seller,
            'listing': proposal.listing
        }
    )
    
    # علامت‌گذاری پیام‌های خوانده نشده
    ChatMessage.objects.filter(
        chat_room=chat_room,
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)
    
    context = {
        'proposal': proposal,
        'chat_room': chat_room,
        'other_user': proposal.seller if request.user == proposal.buyer else proposal.buyer
    }
    return render(request, 'payments/chat.html', context)


@login_required
def get_chat_messages(request, proposal_id):
    """دریافت پیام‌های چت (AJAX)"""
    proposal = get_object_or_404(PriceProposal, id=proposal_id)
    
    if proposal.buyer != request.user and proposal.seller != request.user:
        return JsonResponse({'error': 'دسترسی غیرمجاز'}, status=403)
    
    try:
        chat_room = ChatRoom.objects.get(proposal=proposal)
    except ChatRoom.DoesNotExist:
        return JsonResponse({'messages': []})
    
    # علامت‌گذاری پیام‌های خوانده نشده
    ChatMessage.objects.filter(
        chat_room=chat_room,
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)
    
    messages_data = []
    for msg in chat_room.messages.all():
        messages_data.append({
            'id': msg.id,
            'sender': msg.sender.username,
            'message': msg.message,
            'is_mine': msg.sender == request.user,
            'created_at': msg.created_at.strftime('%Y/%m/%d %H:%M'),
            'is_read': msg.is_read
        })
    
    return JsonResponse({
        'messages': messages_data,
        'proposal_status': proposal.status,
        'buyer_agreed': proposal.buyer_agreed,
        'seller_agreed': proposal.seller_agreed
    })


@login_required
@require_POST
def send_chat_message(request, proposal_id):
    """ارسال پیام چت (AJAX)"""
    proposal = get_object_or_404(PriceProposal, id=proposal_id)
    
    if proposal.buyer != request.user and proposal.seller != request.user:
        return JsonResponse({'error': 'دسترسی غیرمجاز'}, status=403)
    
    # بررسی وضعیت - اگر کنسل یا تایید شده، نمی‌توان پیام فرستاد
    if proposal.status in ['deal_cancelled']:
        return JsonResponse({'error': 'امکان ارسال پیام در وضعیت "کنسل شد" وجود ندارد'}, status=400)
    
    message_text = request.POST.get('message', '').strip()
    
    if not message_text:
        return JsonResponse({'error': 'پیام نمی‌تواند خالی باشد'}, status=400)
    
    chat_room, created = ChatRoom.objects.get_or_create(
        proposal=proposal,
        defaults={
            'buyer': proposal.buyer,
            'seller': proposal.seller,
            'listing': proposal.listing
        }
    )
    
    chat_message = ChatMessage.objects.create(
        chat_room=chat_room,
        sender=request.user,
        message=message_text
    )
    
    # به‌روزرسانی زمان اتاق چت
    chat_room.updated_at = timezone.now()
    chat_room.save()
    
    return JsonResponse({
        'success': True,
        'message': {
            'id': chat_message.id,
            'sender': chat_message.sender.username,
            'message': chat_message.message,
            'is_mine': True,
            'created_at': chat_message.created_at.strftime('%Y/%m/%d %H:%M'),
            'is_read': chat_message.is_read
        }
    })
