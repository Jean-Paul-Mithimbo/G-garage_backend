from django.contrib import admin
from .models import Employe, Contrat, Planning, Conge, Paiement

@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'poste', 'statut', 'email', 'contact', 'date_embauche')
    list_filter = ('poste', 'statut', 'date_embauche')
    search_fields = ('nom', 'prenom', 'email')

@admin.register(Contrat)
class ContratAdmin(admin.ModelAdmin):
    list_display = ('employe', 'type_contrat', 'date_debut', 'date_fin', 'salaire', 'statut')
    list_filter = ('type_contrat', 'statut', 'date_debut', 'date_fin')
    search_fields = ('employe__nom', 'employe__prenom')

@admin.register(Planning)
class PlanningAdmin(admin.ModelAdmin):
    list_display = ('employe', 'jour', 'heure_debut', 'heure_fin')
    list_filter = ('jour',)
    search_fields = ('employe__nom', 'employe__prenom')

@admin.register(Conge)
class CongeAdmin(admin.ModelAdmin):
    list_display = ('employe', 'date_debut', 'date_fin', 'statut')
    list_filter = ('statut', 'date_debut', 'date_fin')
    search_fields = ('employe__nom', 'employe__prenom')

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('employe', 'mois', 'annee', 'salaire_net')
    list_filter = ('mois', 'annee')
    search_fields = ('employe__nom', 'employe__prenom')
