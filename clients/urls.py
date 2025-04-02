from django.urls import path
from .views import (
    ListeClients, DetailClient, ListeDevis, ListeFactures, ListePaiements, 
    ListeAbonnements, ListeFidelites, VerifierStatutFacture
)

urlpatterns = [
    path('clients/', ListeClients.as_view(), name='liste_clients'),
    path('clients/<int:pk>/', DetailClient.as_view(), name='detail_client'),
    path('devis/', ListeDevis.as_view(), name='liste_devis'),
    path('factures/', ListeFactures.as_view(), name='liste_factures'),
    path('paiements/', ListePaiements.as_view(), name='liste_paiements'),
    path('abonnements/', ListeAbonnements.as_view(), name='liste_abonnements'),
    path('fidelites/', ListeFidelites.as_view(), name='liste_fidelites'),
    path('factures/<int:pk>/statut/', VerifierStatutFacture.as_view(), name='verifier_statut_facture'),
]
