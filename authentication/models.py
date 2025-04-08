from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from phonenumbers import parse, is_valid_number, NumberParseException

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

    # Réintégration des champs username et last_name
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True)

    # Utilisation de contact comme identifiant principal
    USERNAME_FIELD = 'contact'
    REQUIRED_FIELDS = ['username', 'email', 'first_name', 'last_name']

    def save(self, *args, **kwargs):
        if isinstance(self.contact, int):
            raise ValueError("Le champ 'contact' doit être une chaîne de caractères valide.")
        try:
            parsed_number = parse(self.contact, "CD")
            if not is_valid_number(parsed_number):
                raise ValueError("Le numéro de téléphone fourni n'est pas valide.")
        except NumberParseException:
            raise ValueError("Le numéro de téléphone fourni n'est pas valide.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.contact} - {self.role}"
