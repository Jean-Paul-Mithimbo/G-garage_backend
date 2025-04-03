from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# 🔹 Étend le modèle d'utilisateur par défaut
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('mecanicien', 'Mécanicien'),
        ('receptionniste', 'Réceptionniste'),
        ('comptable', 'Comptable'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='mecanicien')
    contact = PhoneNumberField(unique=True, blank=False, region="CD")

    def __str__(self):
        return f"{self.username} - {self.role}"
