from django.contrib import admin
from .models import Client, Devis, Facture, Paiement, Abonnement, Fidélité

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'contact', 'historique_interventions')
    search_fields = ('nom', 'contact')

@admin.register(Devis)
class DevisAdmin(admin.ModelAdmin):
    list_display = ('client', 'montant', 'date_creation', 'date_validite', 'statut')
    list_filter = ('statut', 'date_creation')
    search_fields = ('client__nom',)

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('client', 'montant', 'date_creation', 'date_echeance', 'statut')
    list_filter = ('statut', 'date_creation')
    search_fields = ('client__nom',)

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('facture', 'montant', 'date_paiement')
    list_filter = ('date_paiement',)
    search_fields = ('facture__client__nom',)

@admin.register(Abonnement)
class AbonnementAdmin(admin.ModelAdmin):
    list_display = ('client', 'date_debut', 'date_fin', 'type_abonnement')
    list_filter = ('type_abonnement', 'date_debut', 'date_fin')
    search_fields = ('client__nom',)

@admin.register(Fidélité)
class FideliteAdmin(admin.ModelAdmin):
    list_display = ('client', 'points', 'date_dernier_point')
    list_filter = ('date_dernier_point',)
    search_fields = ('client__nom',)

