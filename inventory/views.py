from rest_framework import viewsets, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters

from .models import SparePart, SparePartTrace
from .serializers import (
    SparePartSerializer,
    SparePartTraceSerializer,
    SparePartComparatorSerializer,
)
from .permissions import EstVendeurOuLectureSeule



# 🎯 Filtre personnalisé : expose les champs FR au lieu de EN
class SparePartFilter(django_filters.FilterSet):
    prix = django_filters.NumberFilter(field_name="price")
    localisation = django_filters.CharFilter(field_name="location", lookup_expr="icontains")
    numero_serie = django_filters.CharFilter(field_name="part_number")
    stock_disponible = django_filters.NumberFilter(field_name="stock")
    qualite = django_filters.CharFilter(field_name="quality")
    type_fournisseur = django_filters.CharFilter(field_name="vendor_type")

    class Meta:
        model = SparePart
        fields = ["prix", "localisation", "numero_serie", "stock_disponible", "qualite", "type_fournisseur"]


# 🚘 API Pièces de rechange (catalogue B2B/B2C)
class SparePartViewSet(viewsets.ModelViewSet):
    queryset = SparePart.objects.all()
    serializer_class = SparePartSerializer
    permission_classes = [EstVendeurOuLectureSeule]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SparePartFilter

    # Recherche (nom + description)
    search_fields = ["name", "description"]
    # Tri possible par prix ou stock
    ordering_fields = ["price", "stock"]


# 🔗 API Traçabilité (SIV / Blockchain)
class SparePartTraceViewSet(viewsets.ModelViewSet):
    queryset = SparePartTrace.objects.all()
    serializer_class = SparePartTraceSerializer
    permission_classes = [EstVendeurOuLectureSeule]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtrer par pièce
    filterset_fields = ["spare_part"]
    # Recherche par description
    search_fields = ["event_description"]
    # Tri par date
    ordering_fields = ["timestamp"]


# 🆕 API Comparateur Qualité/Prix
class SparePartComparatorView(generics.ListAPIView):
    queryset = SparePart.objects.all()
    serializer_class = SparePartComparatorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = SparePartFilter
    ordering_fields = ["price", "stock"]






