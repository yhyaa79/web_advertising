# payments/urls.py

from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('purchase/<int:listing_pk>/', views.initiate_purchase, name='initiate_purchase'),
    path('proposal/<int:proposal_id>/', views.proposal_detail, name='proposal_detail'),
    
    path('proposal/<int:proposal_id>/agree/', views.agree_to_deal, name='agree_to_deal'),
    path('proposal/<int:proposal_id>/cancel/', views.cancel_deal, name='cancel_deal'),
    
    path('gateway/<int:transaction_id>/', views.payment_gateway, name='payment_gateway'),
    path('transaction/<int:transaction_id>/', views.transaction_detail, name='transaction_detail'),
    path('confirm/<int:transaction_id>/', views.confirm_delivery, name='confirm_delivery'),
    path('my-transactions/', views.my_transactions, name='my_transactions'),
    path('dispute/<int:transaction_id>/', views.open_dispute, name='open_dispute'),
    
    # چت
    path('chat/<int:proposal_id>/', views.chat_view, name='chat_view'),
    path('chat/<int:proposal_id>/messages/', views.get_chat_messages, name='get_chat_messages'),
    path('chat/<int:proposal_id>/send/', views.send_chat_message, name='send_chat_message'),
]
