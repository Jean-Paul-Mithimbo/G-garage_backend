from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (
    ClientViewSet,DevisViewSet,FidelitesViewSets,AbonnementsViewSet
)

router = DefaultRouter()
router.register('client',ClientViewSet )
router.register('devis',DevisViewSet )
router.register('fidelite',FidelitesViewSets )
router.register('abonnement', AbonnementsViewSet)

urlpatterns = [
    path('', include(router.urls))
]
