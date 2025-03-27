from django.contrib import admin
from .models import Client, Vehicule, Panne, EquipeReparation, Intervention, HistoriqueReparation

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'contact')
    search_fields = ('nom', 'contact')

@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('client', 'marque', 'modele', 'immatriculation', 'annee')
    search_fields = ('immatriculation', 'marque', 'modele')
    list_filter = ('annee',)

@admin.register(Panne)
class PanneAdmin(admin.ModelAdmin):
    list_display = ('vehicule', 'description', 'date_signalement')
    search_fields = ('vehicule__immatriculation',)
    list_filter = ('date_signalement',)

@admin.register(EquipeReparation)
class EquipeReparationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'specialite')
    search_fields = ('nom',)

@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ('panne', 'equipe', 'date_debut', 'date_fin_prevue', 'date_fin_reelle', 'statut')
    list_filter = ('statut', 'date_debut')
    search_fields = ('panne__vehicule__immatriculation',)

@admin.register(HistoriqueReparation)
class HistoriqueReparationAdmin(admin.ModelAdmin):
    list_display = ('intervention', 'date_archivage')
    search_fields = ('intervention__panne__vehicule__immatriculation',)

