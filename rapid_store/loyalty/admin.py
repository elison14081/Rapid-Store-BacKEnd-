from django.contrib import admin
from .models import LoyaltyProfile, LoyaltyTransaction

class LoyaltyTransactionInline(admin.TabularInline):
    model = LoyaltyTransaction
    extra = 0
    readonly_fields = ('description', 'points_changed', 'created_at')
    can_delete = False

@admin.register(LoyaltyProfile)
class LoyaltyProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'points')
    search_fields = ('user__email',)
    inlines = [LoyaltyTransactionInline]

@admin.register(LoyaltyTransaction)
class LoyaltyTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'description', 'points_changed', 'created_at')
    search_fields = ('profile__user__email', 'description')
    list_filter = ('created_at',)