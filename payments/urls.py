from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WalletViewSet, TransactionViewSet, RefundRequestViewSet

router = DefaultRouter()
router.register(r'wallet', WalletViewSet, basename='wallet')
router.register(r'transactions', TransactionViewSet)
router.register(r'refunds', RefundRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
