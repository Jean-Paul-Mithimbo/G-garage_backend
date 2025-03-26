from rest_framework import serializers
from .models import Employe, Contrat, Planning, Conge, Paiement

class EmployeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employe
        fields = '__all__'

class ContratSerializer(serializers.ModelSerializer):
    employe_nom = serializers.CharField(source='employe.nom', read_only=True)
    employe_prenom = serializers.CharField(source='employe.prenom', read_only=True)

    class Meta:
        model = Contrat
        fields = ['id', 'employe', 'employe_nom', 'employe_prenom', 'type_contrat', 'date_debut', 'date_fin', 'salaire', 'statut']

class PlanningSerializer(serializers.ModelSerializer):
    employe_nom = serializers.CharField(source='employe.nom', read_only=True)
    employe_prenom = serializers.CharField(source='employe.prenom', read_only=True)

    class Meta:
        model = Planning
        fields = ['id', 'employe', 'employe_nom', 'employe_prenom', 'jour', 'heure_debut', 'heure_fin']

class CongeSerializer(serializers.ModelSerializer):
    employe_nom = serializers.CharField(source='employe.nom', read_only=True)
    employe_prenom = serializers.CharField(source='employe.prenom', read_only=True)

    class Meta:
        model = Conge
        fields = ['id', 'employe', 'employe_nom', 'employe_prenom', 'date_debut', 'date_fin', 'motif', 'statut']

class PaiementSerializer(serializers.ModelSerializer):
    employe_nom = serializers.CharField(source='employe.nom', read_only=True)
    employe_prenom = serializers.CharField(source='employe.prenom', read_only=True)

    class Meta:
        model = Paiement
        fields = ['id', 'employe', 'employe_nom', 'employe_prenom', 'mois', 'annee', 'salaire_net']