from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings

class Tresorerie(models.Model):
    TYPE_TRANSACTION_CHOICES = [
        ('entree', 'Entrée de fonds'),
        ('sortie', 'Sortie de fonds'),
    ]

    id = models.AutoField(primary_key=True)
    type_transaction = models.CharField(max_length=10, choices=TYPE_TRANSACTION_CHOICES)
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_type_transaction_display()} - {self.montant}€ ({self.date})"

