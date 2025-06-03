from rest_framework import generics, permissions
from .models import LoyaltyProfile, LoyaltyTransaction
from .serializers import LoyaltyProfileSerializer, LoyaltyTransactionSerializer

class LoyaltyProfileView(generics.RetrieveAPIView):
    serializer_class = LoyaltyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return LoyaltyProfile.objects.get(user=self.request.user)

class LoyaltyTransactionListView(generics.ListAPIView):
    serializer_class = LoyaltyTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LoyaltyTransaction.objects.filter(profile__user=self.request.user).order_by('-created_at')
