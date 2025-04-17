from django.urls import path
from .views import (
    ListeStock, DetailStock, ListeFournisseurs, CreerCommande, AjouterProduitCommande,
    MarquerCommandeLivree, ListeCommandes
)

urlpatterns = [
    path('stock/', ListeStock.as_view(), name='liste_stock'),
    path('stock/<int:pk>/', DetailStock.as_view(), name='detail_stock'),
    path('fournisseurs/', ListeFournisseurs.as_view(), name='liste_fournisseurs'),
    path('commandes/', ListeCommandes.as_view(), name='liste_commandes'),
    path('commandes/creer/<int:fournisseur_id>/', CreerCommande.as_view(), name='creer_commande'),
    path('commandes/<int:commande_id>/ajouter-produit/<int:stock_id>/<int:quantite>/', 
         AjouterProduitCommande.as_view(), name='ajouter_produit_commande'),
    path('commandes/<int:commande_id>/livree/', MarquerCommandeLivree.as_view(), name='marquer_commande_livree'),
]
