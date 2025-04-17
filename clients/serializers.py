from rest_framework import serializers
from .models import Client, Devis, Abonnement, Fidélité

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class DevisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devis
        fields = '__all__'

# class FactureSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Facture
#         fields = '__all__'

# class PaiementSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Paiement
#         fields = '__all__'

class AbonnementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abonnement
        fields = '__all__'

class FideliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fidélité
        fields = '__all__'
