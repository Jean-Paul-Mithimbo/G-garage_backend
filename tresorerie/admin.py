from django.contrib import admin
from .models import Tresorerie

@admin.register(Tresorerie)
class TresorerieAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_transaction', 'montant', 'date', 'utilisateur')
    list_filter = ('type_transaction', 'date')
    search_fields = ('description', 'utilisateur__username')
