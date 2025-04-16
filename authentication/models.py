from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from phonenumbers import parse, is_valid_number, NumberParseException

# 🔹 Étend le modèle d'utilisateur par défaut
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('gerant', 'Gérant'),
        ('receptionniste', 'Réceptionniste'),
        ('comptable', 'Comptable'),
        ('autre', 'Autre'),
        
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='autre')
    contact = PhoneNumberField(unique=True, blank=False, region="CD")

    # Réintégration des champs username et last_name
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True)

    # Utilisation de contact comme identifiant principal
    USERNAME_FIELD = 'contact'
    REQUIRED_FIELDS = ['username', 'email', 'first_name', 'last_name']

    def save(self, *args, **kwargs):
        # Convertir le numéro en chaîne pour éviter l'erreur lors du parsing
        contact_str = str(self.contact)
        try:
            parsed_number = parse(contact_str, "CD")  # Parse the number with the region "CD" (Congo)
            if not is_valid_number(parsed_number):  # Check if the number is valid
                raise ValueError("Le numéro de téléphone fourni n'est pas valide.")
        except NumberParseException:
            raise ValueError("Le numéro de téléphone fourni n'est pas valide.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.contact} - {self.role}"
