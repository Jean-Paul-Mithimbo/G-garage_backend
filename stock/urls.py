from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockViewSet, FournisseurViewSet, ArticleViewSet

router = DefaultRouter()
router.register('stocks', StockViewSet)
router.register('fournisseurs', FournisseurViewSet)
router.register('articles', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


# app/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    ArticleViewSet,
    StockViewSet,
    EntreeViewSet,
    SortieViewSet
)

router = DefaultRouter()
router.register('fournisseurs')
router.register('articles', ArticleViewSet, basename='article')
router.register('stocks',   StockViewSet,   basename='stock')
router.register('entrees',  EntreeViewSet,  basename='entree')
router.register('sorties',  SortieViewSet,  basename='sortie')

urlpatterns = [
    # Toutes les routes CRUD générées par DRF
    path('api/', include(router.urls)),
]
