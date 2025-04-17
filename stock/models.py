from django.db import models
from django.utils import timezone

# Modèle Fournisseur
class Fournisseur(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    adresse = models.TextField()
    liste_produits = models.TextField()

    def __str__(self):
        return self.nom

# Modèle Stock (Pièces de rechange)
class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    reference = models.CharField(max_length=100, unique=True)
    nom = models.CharField(max_length=255)
    quantite = models.PositiveIntegerField()
    fournisseur = models.ForeignKey(Fournisseur, related_name='stocks', on_delete=models.CASCADE)
    seuil_alerte = models.PositiveIntegerField(default=10)  # Seuil d'alerte de stock bas

    def est_en_alerte(self):
        return self.quantite <= self.seuil_alerte

    def __str__(self):
        return f"{self.nom} ({self.reference})"

# Modèle Commande
class Commande(models.Model):
    id = models.AutoField(primary_key=True)
    fournisseur = models.ForeignKey(Fournisseur, related_name='commandes', on_delete=models.CASCADE)
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=50, choices=[
        ('en_attente', 'En attente'),
        ('expediee', 'Expédiée'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée')
    ], default='en_attente')

    def __str__(self):
        return f"Commande {self.id} - {self.fournisseur.nom}"

# Modèle DétailCommande (Pièces commandées)
class DétailCommande(models.Model):
    id = models.AutoField(primary_key=True)
    commande = models.ForeignKey(Commande, related_name='details', on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, related_name='commandes', on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantite} x {self.stock.nom} pour Commande {self.commande.id}"

# Modèle Livraison
class Livraison(models.Model):
    id = models.AutoField(primary_key=True)
    commande = models.OneToOneField(Commande, related_name='livraison', on_delete=models.CASCADE)
    date_livraison = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=50, choices=[
        ('en_cours', 'En cours'),
        ('livree', 'Livrée'),
        ('retournee', 'Retournée')
    ], default='en_cours')

    def __str__(self):
        return f"Livraison {self.id} - {self.commande.fournisseur.nom}"

# Modèle Retour (Pièces retournées)
class Retour(models.Model):
    id = models.AutoField(primary_key=True)
    livraison = models.ForeignKey(Livraison, related_name='retours', on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, related_name='retours', on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    raison = models.TextField()

    def __str__(self):
        return f"Retour {self.id} - {self.stock.nom} ({self.quantite})"
