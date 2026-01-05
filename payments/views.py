from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Wallet, Transaction, RefundRequest
from .serializers import WalletSerializer, TransactionSerializer, RefundRequestSerializer
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .permissions import IsVendorOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class WalletViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        wallet = Wallet.objects.get(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsVendorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['wallet__user__id']

def perform_create(self, serializer):
    wallet = Wallet.objects.get(user=self.request.user)
    data = serializer.validated_data
    amount = data['amount']
    transaction_type = data['transaction_type']

    # ✅ Overdraft check
    if transaction_type == 'debit' and wallet.balance < amount:
        from rest_framework.exceptions import ValidationError
        raise ValidationError("Insufficient balance for this transaction.")

    serializer.save(wallet=wallet)


class RefundRequestViewSet(viewsets.ModelViewSet):
    queryset = RefundRequest.objects.all()
    serializer_class = RefundRequestSerializer
    permission_classes = [IsVendorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

