from django.contrib import admin
from .models import Fournisseur, Stock, Commande, DétailCommande, Livraison, Retour

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'contact', 'adresse')
    search_fields = ('nom', 'contact')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('nom', 'reference', 'quantite', 'fournisseur', 'seuil_alerte', 'est_en_alerte')
    search_fields = ('reference', 'nom')
    list_filter = ('fournisseur',)

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'fournisseur', 'date_commande', 'statut')
    list_filter = ('statut', 'date_commande')
    search_fields = ('fournisseur__nom',)

@admin.register(DétailCommande)
class DétailCommandeAdmin(admin.ModelAdmin):
    list_display = ('commande', 'stock', 'quantite')
    search_fields = ('commande__id', 'stock__nom')

@admin.register(Livraison)
class LivraisonAdmin(admin.ModelAdmin):
    list_display = ('commande', 'date_livraison', 'statut')
    list_filter = ('statut',)
    search_fields = ('commande__id',)

@admin.register(Retour)
class RetourAdmin(admin.ModelAdmin):
    list_display = ('livraison', 'stock', 'quantite', 'raison')
    search_fields = ('livraison__id', 'stock__nom')

