from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase
from rest_framework import status
from payments.models import Wallet
from rest_framework_simplejwt.tokens import RefreshToken

class OverdraftProtectionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='vendor_test', password='pass1234')
        group, _ = Group.objects.get_or_create(name='Vendor')
        self.user.groups.add(group)

        self.wallet = Wallet.objects.get(user=self.user)
        self.wallet.balance = 50.00
        self.wallet.save()

        # ✅ Get JWT token and set it in client header
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_debit_overdraft_should_fail(self):
        url = "/api/otopay/transactions/"
        data = {
            "amount": 100.00,
            "transaction_type": "debit",
            "description": "Trying to overdraft"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Insufficient balance", str(response.data))

from payments.models import Transaction, RefundRequest

class RefundWorkflowTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='vendor_refund', password='pass1234')
        group, _ = Group.objects.get_or_create(name='Vendor')
        self.user.groups.add(group)

        # Wallet setup
        self.wallet = Wallet.objects.get(user=self.user)
        self.wallet.balance = 100.00
        self.wallet.save()

        # Authenticate via JWT
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # Create a debit transaction to refund
        self.transaction = Transaction.objects.create(
            wallet=self.wallet,
            amount=40.00,
            transaction_type='debit',
            description='Test debit to refund'
        )

    def test_refund_restores_wallet_balance(self):
        # Create refund request
        refund = RefundRequest.objects.create(transaction=self.transaction)

        # Approve the refund
        refund.approve()

        # Refresh wallet
        self.wallet.refresh_from_db()

        # Expected balance = 100.00 (original) -

class CreditTransactionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='vendor_credit', password='pass1234')
        group, _ = Group.objects.get_or_create(name='Vendor')
        self.user.groups.add(group)

        self.wallet = Wallet.objects.get(user=self.user)
        self.wallet.balance = 20.00
        self.wallet.save()

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_credit_transaction_updates_balance(self):
        url = "/api/otopay/transactions/"
        data = {
            "amount": 50.00,
            "transaction_type": "credit",
            "description": "Vendor top-up test"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 70.00)  # 20 + 50


