from django.contrib import admin
from .models import (
    Article, Stock,Fournisseurs
    Entree, LigneEntree,
    Sortie, LigneSortie
)

# Inline pour les lignes d'entrée
class LigneEntreeInline(admin.TabularInline):
    model = LigneEntree
    extra = 1
    fields = (
        'article',
        'quantite',
        'prix_unitaire',
        'date_expiration',
        'date_entree',
    )
    readonly_fields = ('date_entree',)

# Admin pour Entree
@admin.register(Entree)
class EntreeAdmin(admin.ModelAdmin):
    list_display = ('id', 'libele', 'date_op')
    list_filter  = ('date_op',)
    search_fields = ('libele',)
    inlines = (LigneEntreeInline,)


# Inline pour les lignes de sortie
class LigneSortieInline(admin.TabularInline):
    model = LigneSortie
    extra = 1
    fields = (
        'article',
        'quantite',
        'date_sortie',
    )
    readonly_fields = ('date_sortie',)

# Admin pour Sortie
@admin.register(Sortie)
class SortieAdmin(admin.ModelAdmin):
    list_display = ('id', 'motif')
    search_fields = ('motif',)
    inlines = (LigneSortieInline,)


# Admin pour Article
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom',)
    search_fields = ('nom',)
    # Permet de naviguer vers le stock lié
    readonly_fields = ()
    # Optionnel : afficher le stock courant en liste
    def stock_quantite(self, obj):
        return obj.stock.quantite
    stock_quantite.short_description = 'Quantité en stock'
    list_display += ('stock_quantite',)


# Admin pour Stock
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('article', 'quantite', 'seuil_alerte')
    list_filter  = ('seuil_alerte',)
    search_fields = ('article__nom',)

# Admin pour Stock
@admin.register(Fournisseurs)
class FournisseursAdmin(admin.ModelAdmin):
    list_display = ('nom', 'contact', 'adresse')
    list_filter  = ('nom',)
    search_fields = ('nom',)

