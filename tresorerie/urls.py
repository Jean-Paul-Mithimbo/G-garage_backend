from django.urls import path
from .views import ListeTresorerie, DetailTresorerie, AjouterTransaction, RapportFinancier

urlpatterns = [
    path('tresorerie/', ListeTresorerie.as_view(), name='liste_tresorerie'),
    path('tresorerie/<int:pk>/', DetailTresorerie.as_view(), name='detail_tresorerie'),
    path('tresorerie/ajouter/', AjouterTransaction.as_view(), name='ajouter_transaction'),
    path('tresorerie/rapport/', RapportFinancier.as_view(), name='rapport_financier'),
]
