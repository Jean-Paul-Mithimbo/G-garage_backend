# from rest_framework import serializers
# from .models import Stock, Fournisseur, Article

# class ArticleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Article
#         fields = ['id', 'nom', 'description', 'caracteristiques']

# class StockSerializer(serializers.ModelSerializer):
#     article = ArticleSerializer(read_only=True)

#     class Meta:
#         model = Stock
#         fields = ['id', 'article', 'quantite', 'seuil_alerte', 'prix_unitaire']

# class FournisseurSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Fournisseur
#         fields = '__all__'


from rest_framework import serializers
from .models import (
    Fournisseur,
    Article, Stock,
    Entree, LigneEntree,
    Sortie, LigneSortie
)

class FournisseursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fournisseurs
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Article
        fields = ['id', 'nom', 'description']

class StockSerializer(serializers.ModelSerializer):
    article = serializers.StringRelatedField()
    class Meta:
        model  = Stock
        fields = ['id', 'article', 'quantite', 'seuil_alerte']

class LigneEntreeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = LigneEntree
        fields = [
            'id', 'article', 'quantite', 'prix_unitaire',
            'date_entree', 'date_expiration'
        ]

class EntreeSerializer(serializers.ModelSerializer):
    lignes = LigneEntreeSerializer(many=True)
    class Meta:
        model  = Entree
        fields = ['id', 'libele','date_op', 'lignes']

class LigneSortieSerializer(serializers.ModelSerializer):
    class Meta:
        model  = LigneSortie
        fields = [
            'id', 'article', 'quantite', 'date_sortie'
        ]

class SortieSerializer(serializers.ModelSerializer):
    lignes = LigneSortieSerializer(many=True)
    class Meta:
        model  = Sortie
        fields = ['id', 'motif', 'lignes']
