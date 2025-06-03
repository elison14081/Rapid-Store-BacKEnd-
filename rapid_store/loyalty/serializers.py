from rest_framework import serializers
from .models import LoyaltyProfile, LoyaltyTransaction

class LoyaltyTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyTransaction
        fields = ['id', 'description', 'points_changed', 'created_at']

class LoyaltyProfileSerializer(serializers.ModelSerializer):
    transactions = LoyaltyTransactionSerializer(many=True, read_only=True)

    class Meta:
        model = LoyaltyProfile
        fields = ['id', 'user', 'points', 'transactions']
        read_only_fields = ['user', 'points', 'transactions']
