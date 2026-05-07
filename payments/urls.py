# payments/urls.py

from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('purchase/<int:listing_pk>/', views.initiate_purchase, name='initiate_purchase'),
    path('my-proposals/', views.my_proposals, name='my_proposals'),
    path('proposal/<int:proposal_id>/', views.proposal_detail, name='proposal_detail'),
    path('proposal/<int:proposal_id>/respond/', views.respond_to_proposal, name='respond_to_proposal'),
    path('gateway/<int:transaction_id>/', views.payment_gateway, name='payment_gateway'),
    path('transaction/<int:transaction_id>/', views.transaction_detail, name='transaction_detail'),
    path('confirm/<int:transaction_id>/', views.confirm_delivery, name='confirm_delivery'),
    path('my-transactions/', views.my_transactions, name='my_transactions'),
    path('dispute/<int:transaction_id>/', views.open_dispute, name='open_dispute'),
]
