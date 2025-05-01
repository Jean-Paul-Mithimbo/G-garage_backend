from django.contrib import admin
from .models import (
    Vehicule, Panne, Intervention, LignePanne, MaterielUtilise, Facture, HistoriqueReparation
)

@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ['marque', 'modele']
    search_fields = ['marque', 'modele']

@admin.register(Panne)
class PanneAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom','description']
    search_fields = ['description']

@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ['id', 'vehicule','immatriculation','client','equipe', 'date_debut','date_fin_prevue','date_fin_reelle', 'statut']
    list_filter = ['statut', 'equipe']
    search_fields = ['vehicule__immatriculation']

@admin.register(LignePanne)
class LignePanneAdmin(admin.ModelAdmin):
    list_display = ['id', 'intervention', 'panne','description','date_signalement']
    search_fields = ['panne__description']

@admin.register(MaterielUtilise)
class MaterielUtiliseAdmin(admin.ModelAdmin):
    list_display = ['id', 'intervention', 'stock', 'quantite']
    search_fields = ['stock__article__nom']

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ['id', 'intervention', 'montant_main_oeuvre', 'date_emission', 'statut']
    list_filter = ['statut']
    search_fields = ['intervention__vehicule__immatriculation']

@admin.register(HistoriqueReparation)
class HistoriqueReparationAdmin(admin.ModelAdmin):
    list_display = ['id', 'intervention', 'date_archivage']
    search_fields = ['intervention__vehicule__immatriculation']

