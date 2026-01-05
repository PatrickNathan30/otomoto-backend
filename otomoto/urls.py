"""
Configuration des URLs pour le projet Otomoto.

La liste `urlpatterns` dirige les URLs vers les vues. Pour plus d’informations, voir :
    https://docs.djangoproject.com/fr/5.2/topics/http/urls/
Exemples :
Vues basées sur des fonctions
    1. Importer :  from my_app import views
    2. Ajouter une URL :  path('', views.home, name='home')
Vues basées sur des classes
    1. Importer :  from other_app.views import Home
    2. Ajouter une URL :  path('', Home.as_view(), name='home')
Inclure une autre configuration d’URL
    1. Importer include : from django.urls import include, path
    2. Ajouter une URL :  path('blog/', include('blog.urls'))
"""
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from inventory.views import SparePartViewSet, SparePartTraceViewSet, SparePartComparatorView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# 🔧 Enregistrer vos ViewSets API
router = DefaultRouter()
router.register(r'pieces', SparePartViewSet, basename='pieces')  # ⚙️ Pièces de rechange
router.register(r'traces-pieces', SparePartTraceViewSet, basename='traces-pieces')  # ⚙️ Traçabilités de pièces

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/otopay/', include('payments.urls')),

    path('api/comparateur/', SparePartComparatorView.as_view(), name='comparateur'),  # ⚙️ Nouvel endpoint
]

# 📄 Documentation Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="API OtoPay",
      default_version='v1',
      description="Documentation pour Portefeuilles, Transactions, Remboursements",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]




