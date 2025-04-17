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
