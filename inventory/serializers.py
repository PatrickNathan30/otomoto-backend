from rest_framework import serializers
from .models import SparePart, SparePartTrace

# 🔧 Sérialiseur basique
class SparePartSerializer(serializers.ModelSerializer):
    class Meta:
        model = SparePart
        fields = '__all__'


# 🔍 Sérialiseur de traçabilité
class SparePartTraceSerializer(serializers.ModelSerializer):
    piece_de_rechange = SparePartSerializer(read_only=True, source='spare_part')
    piece_de_rechange_id = serializers.PrimaryKeyRelatedField(
        queryset=SparePart.objects.all(),
        source='spare_part',
        write_only=True
    )

    class Meta:
        model = SparePartTrace
        fields = '__all__'
        extra_kwargs = {
            'event_description': {'label': 'Description de l’événement'},
            'timestamp': {'label': 'Horodatage'},
            'previous_hash': {'label': 'Hash précédent'},
            'current_hash': {'label': 'Hash actuel'},
        }


# 📊 Sérialiseur comparateur
class SparePartComparatorSerializer(serializers.ModelSerializer):
    taux_defaut = serializers.SerializerMethodField(label="Taux de défaut")

    class Meta:
        model = SparePart
        fields = [
            'id',
            'name',          # 👈 si tu veux : remplacer par "nom"
            'price',         # 👈 remplacer par "prix"
            'quality',       # 👈 remplacer par "qualité"
            'vendor_type',   # 👈 remplacer par "type_fournisseur"
            'stock',         # 👈 remplacer par "stock_disponible"
            'taux_defaut'
        ]
        extra_kwargs = {
            'name': {'label': 'Nom de la pièce'},
            'price': {'label': 'Prix (MAD)'},
            'quality': {'label': 'Qualité'},
            'vendor_type': {'label': 'Type de fournisseur'},
            'stock': {'label': 'Stock disponible'},
        }

    def get_taux_defaut(self, obj):
        total_traces = obj.traces.count()
        defectueux = obj.traces.filter(event_description__icontains='defect').count()
        if total_traces == 0:
            return "0%"
        return f"{(defectueux / total_traces) * 100:.1f}%"


