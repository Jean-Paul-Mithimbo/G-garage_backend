from rest_framework import serializers
from .models import (
    Vehicule, Panne, EquipeReparation,Intervention, LignePanne, MaterielUtilise, Facture, HistoriqueReparation
)

class VehiculeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicule
        fields = '__all__'

class PanneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panne
        fields = '__all__'
class EquipeReparationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipeReparation
        fields = '__all__'

class InterventionSerializer(serializers.ModelSerializer):
    lignes_pannes = serializers.StringRelatedField(many=True, read_only=True)
    materiels_utilises = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Intervention
        fields = '__all__'

class LignePanneSerializer(serializers.ModelSerializer):
    class Meta:
        model = LignePanne
        fields = '__all__'

class MaterielUtiliseSerializer(serializers.ModelSerializer):
    stock = serializers.StringRelatedField()

    class Meta:
        model = MaterielUtilise
        fields = ['id', 'intervention', 'stock', 'quantite']

class FactureSerializer(serializers.ModelSerializer):
    montant_total = serializers.SerializerMethodField()

    class Meta:
        model = Facture
        fields = ['id', 'intervention', 'montant_main_oeuvre', 'date_emission', 'statut', 'montant_total']

    def get_montant_total(self, obj):
        return obj.calculer_montant_total()

class HistoriqueReparationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriqueReparation
        fields = '__all__'
