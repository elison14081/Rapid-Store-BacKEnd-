from django.urls import path
from .views import LoyaltyProfileView, LoyaltyTransactionListView

urlpatterns = [
    path('profile/', LoyaltyProfileView.as_view(), name='loyalty-profile'),
    path('transactions/', LoyaltyTransactionListView.as_view(), name='loyalty-transactions'),
]
