from rest_framework import serializers
from .models import Client, Vehicule, Panne, EquipeReparation, Intervention, HistoriqueReparation

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

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
    class Meta:
        model = Intervention
        fields = '__all__'

class HistoriqueReparationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriqueReparation
        fields = '__all__'
