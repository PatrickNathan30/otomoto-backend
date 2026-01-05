from rest_framework import serializers
from .models import Wallet, Transaction, RefundRequest
from .models import Transaction, Wallet

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'balance', 'updated_at']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'wallet', 'amount', 'transaction_type', 'timestamp', 'description']
        read_only_fields = ['wallet', 'timestamp', 'id']

    def validate(self, data):
        request = self.context['request']
        wallet = Wallet.objects.get(user=request.user)

        if data['transaction_type'] == 'debit' and wallet.balance < data['amount']:
            raise serializers.ValidationError("Insufficient balance for this transaction.")

        return data

    def create(self, validated_data):
        wallet = Wallet.objects.get(user=self.context['request'].user)
        validated_data['wallet'] = wallet
        return super().create(validated_data)

        
class RefundRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefundRequest
        fields = ['id', 'transaction', 'requested_at', 'approved']
        read_only_fields = ['approved']
