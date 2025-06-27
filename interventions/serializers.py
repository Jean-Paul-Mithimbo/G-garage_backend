from rest_framework import serializers
from .models import (
    Vehicule, Panne, EquipeReparation,Intervention, LignePanne, MaterielUtilise, Facture, HistoriqueReparation,InterventionDraft
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

class LignePanneSerializer(serializers.ModelSerializer):
    panne = PanneSerializer(read_only=True)
    class Meta:
        model = LignePanne
        fields = ['id', 'intervention', 'panne', 'description', 'date_signalement']

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

class InterventionSerializer(serializers.ModelSerializer):
    lignes_pannes = LignePanneSerializer(many=True, read_only=True)
    materiels_utilises = MaterielUtiliseSerializer(many=True, read_only=True)
    facture = FactureSerializer(read_only=True)
    class Meta:
        model = Intervention
        fields = '__all__'

# class InterventionDraftSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InterventionDraft
#         fields = ['id', 'user', 'data', 'created_at', 'updated_at']
#         read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class InterventionDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterventionDraft
        fields = ['id', 'user', 'data', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class HistoriqueReparationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriqueReparation
        fields = '__all__'
