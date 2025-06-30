
from django.contrib import admin
from .models import (
    Vehicule, Panne, EquipeReparation, Intervention, LignePanne,
    MaterielUtilise, Facture, HistoriqueReparation, InterventionDraft
)

# Inlines for related models
class LignePanneInline(admin.TabularInline):
    model = LignePanne
    extra = 1

class MaterielUtiliseInline(admin.TabularInline):
    model = MaterielUtilise
    extra = 1

class FactureInline(admin.StackedInline):
    model = Facture
    extra = 0
    max_num = 1

# Main admin for Intervention
@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ['id', 'vehicule', 'client', 'equipe', 'date_debut', 'statut']
    list_filter = ['statut', 'equipe']
    search_fields = ['vehicule__immatriculation', 'client__nom']
    inlines = [LignePanneInline, MaterielUtiliseInline, FactureInline]

# Inline for interventions in Vehicule admin
class InterventionInline(admin.TabularInline):
    model = Intervention
    extra = 1

@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ['id', 'marque', 'modele']
    inlines = [InterventionInline]
    search_fields = ['marque', 'modele']

@admin.register(Panne)
class PanneAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'description']
    search_fields = ['nom', 'description']

@admin.register(EquipeReparation)
class EquipeReparationAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'specialite']
    search_fields = ['nom', 'specialite']

@admin.register(LignePanne)
class LignePanneAdmin(admin.ModelAdmin):
    list_display = ['id', 'intervention', 'panne', 'description', 'date_signalement']
    search_fields = ['description']
    list_filter = ['date_signalement']

@admin.register(MaterielUtilise)
class MaterielUtiliseAdmin(admin.ModelAdmin):
    list_display = ['id', 'intervention', 'stock', 'quantite']
    search_fields = ['stock__article__nom']
    list_filter = ['stock']

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ['id', 'intervention', 'montant_main_oeuvre', 'date_emission', 'statut']
    search_fields = ['intervention__vehicule__immatriculation']
    list_filter = ['statut', 'date_emission']

@admin.register(HistoriqueReparation)
class HistoriqueReparationAdmin(admin.ModelAdmin):
    list_display = ['id', 'intervention', 'date_archivage']
    search_fields = ['intervention__vehicule__immatriculation']
    list_filter = ['date_archivage']

@admin.register(InterventionDraft)
class InterventionDraftAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    list_filter = ('created_at', 'updated_at')
