from rest_framework import serializers
from .models import Stock, Fournisseur, Commande, DétailCommande, Livraison, Retour

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class FournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fournisseur
        fields = '__all__'

class CommandeSerializer(serializers.ModelSerializer):
    details = serializers.StringRelatedField(many=True)  # Liste des détails de la commande

    class Meta:
        model = Commande
        fields = '__all__'

class DétailCommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DétailCommande
        fields = '__all__'

class LivraisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livraison
        fields = '__all__'

class RetourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retour
        fields = '__all__'
