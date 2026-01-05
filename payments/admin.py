from django.contrib import admin
from .models import Wallet, Transaction, RefundRequest


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "updated_at")
    list_display_links = ("user",)
    search_fields = ("user__username",)
    ordering = ("-updated_at",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("wallet", "amount", "transaction_type", "timestamp", "description")
    list_filter = ("transaction_type", "timestamp")
    search_fields = ("wallet__user__username", "description")
    ordering = ("-timestamp",)


@admin.register(RefundRequest)
class RefundRequestAdmin(admin.ModelAdmin):
    list_display = ("transaction", "requested_at", "approved")
    list_filter = ("approved", "requested_at")
    ordering = ("-requested_at",)


