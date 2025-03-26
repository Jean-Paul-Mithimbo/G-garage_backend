from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeViewSet, ContratViewSet, PlanningViewSet, CongeViewSet, PaiementViewSet

router = DefaultRouter()
router.register(r'employes', EmployeViewSet)
router.register(r'contrats', ContratViewSet)
router.register(r'plannings', PlanningViewSet)
router.register(r'conges', CongeViewSet)
router.register(r'paiements', PaiementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]