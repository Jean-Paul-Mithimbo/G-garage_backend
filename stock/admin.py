from django.contrib import admin
from .models import Stock, Fournisseur, Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom']
    search_fields = ['nom', 'description']

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'quantite', 'seuil_alerte', 'prix_unitaire']
    search_fields = ['article__nom']

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'contact']
    search_fields = ['nom', 'contact']

