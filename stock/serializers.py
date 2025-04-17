from rest_framework import serializers
from .models import Stock, Fournisseur, Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'nom', 'description', 'caracteristiques']

class StockSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(read_only=True)

    class Meta:
        model = Stock
        fields = ['id', 'article', 'quantite', 'seuil_alerte', 'prix_unitaire']

class FournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fournisseur
        fields = '__all__'
