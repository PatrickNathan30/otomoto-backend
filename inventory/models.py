from django.db import models
import hashlib

class SparePart(models.Model):
    QUALITY_CHOICES = [
        ('ORIGINAL', 'Original'),
        ('ADAPTABLE', 'Adaptable'),
        ('NEUF', 'Neuf'),
        ('OCCASION', 'Occasion'),
    ]
    
    VENDOR_CHOICES = [
        ('Concessionnaire', 'Concessionnaire'),
        ('Equipementier', 'Équipementier'),
        ('Importateur', 'Importateur'),
        ('Grossiste', 'Grossiste'),
        ('Semi-grossiste', 'Semi-grossiste'),
        ('Détaillant', 'Détaillant'),
        ('Ferrailleurs', 'Ferrailleurs'),
        ('Particuliers', 'Particuliers (BtC to C)'),
    ]

    name = models.CharField("Nom de la pièce", max_length=255)
    description = models.TextField("Description")
    part_number = models.CharField("Numéro de série", max_length=100, unique=True)
    stock = models.IntegerField("Stock disponible")
    price = models.DecimalField("Prix (MAD)", max_digits=10, decimal_places=2)
    location = models.CharField("Localisation", max_length=255)

    # Champ qualité avec choix
    quality = models.CharField(
        "Qualité",
        max_length=20,
        choices=QUALITY_CHOICES,
        default='NEUF',  # Défaut : Neuf
    )

    vendor_type = models.CharField(
        "Type de fournisseur",
        max_length=50,
        choices=VENDOR_CHOICES,
        default='Grossiste'
    )

    date_added = models.DateTimeField("Date d’ajout", auto_now_add=True)

    class Meta:
        verbose_name = "Pièce de rechange"
        verbose_name_plural = "Pièces de rechange"

    def __str__(self):
        return self.name


class SparePartTrace(models.Model):
    spare_part = models.ForeignKey(
        SparePart, 
        on_delete=models.CASCADE, 
        related_name='traces',
        verbose_name="Pièce associée"
    )
    timestamp = models.DateTimeField("Horodatage", auto_now_add=True)
    event_description = models.TextField("Description de l’événement")
    previous_hash = models.CharField("Hash précédent", max_length=64, blank=True)
    current_hash = models.CharField("Hash actuel", max_length=64, blank=True)

    class Meta:
        verbose_name = "Traçabilité de pièce"
        verbose_name_plural = "Traçabilités de pièces"

    def save(self, *args, **kwargs):
        if not self.id:
            # Seulement pour les nouveaux enregistrements
            prev_trace = SparePartTrace.objects.filter(spare_part=self.spare_part).order_by('-timestamp').first()
            prev_hash = prev_trace.current_hash if prev_trace else ''
            self.previous_hash = prev_hash

            # Composer les données à hasher
            data = f"{self.previous_hash}{self.event_description}{self.timestamp}"
            self.current_hash = hashlib.sha256(data.encode('utf-8')).hexdigest()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Traçabilité pour {self.spare_part.name} à {self.timestamp}"



