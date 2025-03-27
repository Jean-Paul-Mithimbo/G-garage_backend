from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

# 🔹 Étend le modèle d'utilisateur par défaut
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('mecanicien', 'Mécanicien'),
        ('receptionniste', 'Réceptionniste'),
        ('comptable', 'Comptable'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='mecanicien')
    contact = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.role}"
