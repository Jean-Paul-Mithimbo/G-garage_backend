from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DetailClient, ListeVehicules, ListePannes, EquipesViewSet,
    ListeInterventions, ListeHistoriques, AffecterEquipe, CloturerIntervention,
    VehiculeViewSet, PanneViewSet, InterventionViewSet, LignePanneViewSet,
    MaterielUtiliseViewSet, FactureViewSet, HistoriqueReparationViewSet,
    InterventionDraftViewSet
)

router = DefaultRouter()
router.register('vehicules', VehiculeViewSet)  # Matches VehiculeViewSet in views.py
router.register('pannes', PanneViewSet)  # Matches PanneViewSet in views.py
router.register('equipes', EquipesViewSet)  # equipe
router.register('interventions', InterventionViewSet)  # Matches InterventionViewSet in views.py
router.register('lignes-pannes', LignePanneViewSet)  # Matches LignePanneViewSet in views.py
router.register('materiels-utilises', MaterielUtiliseViewSet)  # Matches MaterielUtiliseViewSet in views.py
router.register('factures', FactureViewSet)  # Matches FactureViewSet in views.py
router.register('historiques-reparations', HistoriqueReparationViewSet)  # Matches HistoriqueReparationViewSet in views.py
router.register('drafts', InterventionDraftViewSet)  # Matches InterventionDraftViewSet in views.py

urlpatterns = [
    path('clients/<int:pk>/', DetailClient.as_view(), name='detail_client'),  # Matches DetailClient in views.py
    # path('vehicules/', ListeVehicules.as_view(), name='liste_vehicules'),  # Matches ListeVehicules in views.py
    # path('pannes/', ListePannes.as_view(), name='liste_pannes'),  # Matches ListePannes in views.py
    # path('equipes/', ListeEquipes.as_view(), name='liste_equipes'),  # Matches ListeEquipes in views.py
    # path('interventions/', ListeInterventions.as_view(), name='liste_interventions'),  # Matches ListeInterventions in views.py
    path('historiques/', ListeHistoriques.as_view(), name='liste_historiques'),  # Matches ListeHistoriques in views.py
    # path('interventions/<int:intervention_id>/affecter/<int:equipe_id>/', AffecterEquipe.as_view(), name='affecter_equipe'),  # Matches AffecterEquipe in views.py
    # path('interventions/<int:intervention_id>/cloturer/', CloturerIntervention.as_view(), name='cloturer_intervention'),  # Matches CloturerIntervention in views.py
    path('', include(router.urls)),  # Includes all viewsets registered in the router
]
