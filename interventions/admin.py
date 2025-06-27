from django.contrib import admin
from .models import (
    Vehicule, Panne, EquipeReparation, Intervention, LignePanne,
    MaterielUtilise, Facture, HistoriqueReparation, InterventionDraft
)

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

@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ['id', 'vehicule', 'client', 'equipe', 'date_debut', 'statut']
    list_filter = ['statut', 'equipe']
    search_fields = ['vehicule__immatriculation']
    inlines = [LignePanneInline, MaterielUtiliseInline, FactureInline]

@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ['id', 'marque', 'modele']

@admin.register(Panne)
class PanneAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'description']

@admin.register(EquipeReparation)
class EquipeReparationAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'specialite']

@admin.register(LignePanne)
class LignePanneAdmin(admin.ModelAdmin):
    list_display = ['id', 'intervention', 'panne', 'description', 'date_signalement']

@admin.register(MaterielUtilise)
class MaterielUtiliseAdmin(admin.ModelAdmin):
    list_display = ['id', 'intervention', 'stock', 'quantite']

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ['id', 'intervention', 'montant_main_oeuvre', 'date_emission', 'statut']

@admin.register(HistoriqueReparation)
class HistoriqueReparationAdmin(admin.ModelAdmin):
    list_display = ['id', 'intervention', 'date_archivage']

# @admin.register(InterventionDraft)
# class InterventionDraftAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'created_at', 'updated_at']

@admin.register(InterventionDraft)
class InterventionDraftAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    list_filter = ('created_at', 'updated_at')