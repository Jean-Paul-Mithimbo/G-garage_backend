from django.urls import path
from .views import (
    ListeClients, DetailClient, ListeVehicules, ListePannes, ListeEquipes,
    ListeInterventions, ListeHistoriques, AffecterEquipe, CloturerIntervention
)

urlpatterns = [
    path('clients/', ListeClients.as_view(), name='liste_clients'),
    path('clients/<int:pk>/', DetailClient.as_view(), name='detail_client'),
    path('vehicules/', ListeVehicules.as_view(), name='liste_vehicules'),
    path('pannes/', ListePannes.as_view(), name='liste_pannes'),
    path('equipes/', ListeEquipes.as_view(), name='liste_equipes'),
    path('interventions/', ListeInterventions.as_view(), name='liste_interventions'),
    path('historiques/', ListeHistoriques.as_view(), name='liste_historiques'),
    path('interventions/<int:intervention_id>/affecter/<int:equipe_id>/', AffecterEquipe.as_view(), name='affecter_equipe'),
    path('interventions/<int:intervention_id>/cloturer/', CloturerIntervention.as_view(), name='cloturer_intervention'),
]
