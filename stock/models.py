from django.db import models

# Modèle Fournisseur
class Fournisseur(models.Model):
    nom = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    adresse = models.TextField()

    def __str__(self):
        return self.nom

# Modèle Article (Caractéristiques des articles)
class Article(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    caracteristiques = models.JSONField(default=dict)  # Store characteristics as key-value pairs

    def __str__(self):
        return self.nom

# Modèle Stock (Gestion du stock des articles)
class Stock(models.Model):
    article = models.OneToOneField(Article, related_name='stock', on_delete=models.CASCADE, null=True, blank=True)  # Allow null values default=1)  # Use the ID of a default Article
    quantite = models.PositiveIntegerField()
    seuil_alerte = models.PositiveIntegerField(default=10)  # Seuil d'alerte de stock bas
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Prix unitaire

    def est_en_alerte(self):
        return self.quantite <= self.seuil_alerte

    def ajouter_quantite(self, quantite):
        """Augmente la quantité en stock."""
        self.quantite += quantite
        self.save()

    def diminuer_quantite(self, quantite):
        """Diminue la quantité en stock."""
        if self.quantite < quantite:
            raise ValueError(f"Stock insuffisant pour {self.article.nom}.")
        self.quantite -= quantite
        self.save()

    def __str__(self):
        return f"Stock de {self.article.nom} - Quantité: {self.quantite}"
