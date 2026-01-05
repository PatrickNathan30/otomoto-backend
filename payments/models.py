from django.db import models
from django.contrib.auth.models import User


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Solde")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")

    class Meta:
        verbose_name = "Portefeuille"
        verbose_name_plural = "Portefeuilles"

    def __str__(self):
        return f"Portefeuille de {self.user.username} - Solde: {self.balance}"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('credit', 'Crédit'),
        ('debit', 'Débit'),
    )

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, verbose_name="Portefeuille")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Montant")
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPES, verbose_name="Type de transaction")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Date de transaction")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # vérifier si c'est une nouvelle transaction

        super().save(*args, **kwargs)  # sauvegarde en BD

        if is_new:
            if self.transaction_type == 'credit':
                self.wallet.balance += self.amount
            elif self.transaction_type == 'debit':
                self.wallet.balance -= self.amount
            self.wallet.save()

    def __str__(self):
        return f"{self.get_transaction_type_display().upper()} - {self.amount} le {self.timestamp}"


class RefundRequest(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, verbose_name="Transaction")
    requested_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de demande")
    approved = models.BooleanField(default=False, verbose_name="Approuvée")

    class Meta:
        verbose_name = "Demande de remboursement"
        verbose_name_plural = "Demandes de remboursement"

    def approve(self):
        if not self.approved:
            self.approved = True
            self.save()
            wallet = self.transaction.wallet
            wallet.balance += self.transaction.amount
            wallet.save()

            Transaction.objects.create(
                wallet=wallet,
                amount=self.transaction.amount,
                transaction_type='credit',
                description=f"Remboursement approuvé pour la transaction #{self.transaction.id}"
            )

    def __str__(self):
        return f"Demande de remboursement pour Tx {self.transaction.id} - Approuvée : {self.approved}"


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_wallet_for_user(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)


