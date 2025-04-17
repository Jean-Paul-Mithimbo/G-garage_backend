from django.db import models
from clients.models import Client
from ressources_humaine.models import Employe
from stock.models import Stock

# # Modèle Client
# class Client(models.Model):
#     id = models.AutoField(primary_key=True)
#     nom = models.CharField(max_length=255)
#     contact = models.CharField(max_length=255)

#     def __str__(self):
#         return self.nom

# Modèle Véhicule
class Vehicule(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, related_name='vehicules', on_delete=models.CASCADE)
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    immatriculation = models.CharField(max_length=50, unique=True)
    annee = models.IntegerField()

    def __str__(self):
        return f"{self.marque} {self.modele} - {self.immatriculation}"

# Modèle Panne
class Panne(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    date_signalement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Panne {self.id} - {self.description[:50]}"

# Modèle Équipe de Réparation
class EquipeReparation(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=255)
    # employes = models.ManyToManyField(Employe, related_name='equipes')  # Many-to-many relationship

    def __str__(self):
        return self.nom

# Modèle Intervention
class Intervention(models.Model):
    id = models.AutoField(primary_key=True)
    vehicule = models.ForeignKey(Vehicule, related_name='interventions', on_delete=models.CASCADE, null=True, blank=True)  # Allow null values
    equipe = models.ForeignKey(EquipeReparation, related_name='interventions', on_delete=models.SET_NULL, null=True)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin_prevue = models.DateTimeField()
    date_fin_reelle = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=50, choices=[('en_cours', 'En cours'), ('terminee', 'Terminée'), ('annulee', 'Annulée')], default='en_cours')

    def __str__(self):
        return f"Intervention {self.id} - {self.vehicule.immatriculation if self.vehicule else 'Aucun véhicule'}"

# Modèle Ligne de Panne
class LignePanne(models.Model):
    id = models.AutoField(primary_key=True)
    intervention = models.ForeignKey(Intervention, related_name='lignes_pannes', on_delete=models.CASCADE)
    panne = models.ForeignKey(Panne, related_name='lignes_pannes', on_delete=models.CASCADE)

    def __str__(self):
        return f"Panne {self.panne.id} liée à Intervention {self.intervention.id}"

# Modèle Matériel utilisé dans une intervention
class MaterielUtilise(models.Model):
    id = models.AutoField(primary_key=True)
    intervention = models.ForeignKey(Intervention, related_name='materiels_utilises', on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, related_name='utilisations', on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        """Diminue le stock lors de l'utilisation de matériel."""
        if not self.pk:  # Only decrease stock on creation
            self.stock.diminuer_quantite(self.quantite)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Restaure le stock si l'utilisation est supprimée."""
        self.stock.ajouter_quantite(self.quantite)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.quantite} x {self.stock.article.nom} pour Intervention {self.intervention.id}"

# Modèle Historique des réparations
class HistoriqueReparation(models.Model):
    id = models.AutoField(primary_key=True)
    intervention = models.OneToOneField(Intervention, related_name='historique', on_delete=models.CASCADE)
    details = models.TextField()
    date_archivage = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Historique de {self.intervention.panne.vehicule.immatriculation}"

# Modèle Facture
class Facture(models.Model):
    id = models.AutoField(primary_key=True)
    intervention = models.OneToOneField(Intervention, related_name='facture', on_delete=models.CASCADE)
    montant_main_oeuvre = models.DecimalField(max_digits=15, decimal_places=2)
    date_emission = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=50, choices=[
        ('payee', 'Payée'),
        ('impayee', 'Imppayée'),
    ], default='impayee')

    def calculer_montant_total(self):
        """Calcule le montant total de la facture (main d'œuvre + matériel)."""
        montant_materiels = sum(
            materiel.quantite * materiel.stock.prix_unitaire
            for materiel in self.intervention.materiels_utilises.all()
        )
        return self.montant_main_oeuvre + montant_materiels

    def __str__(self):
        return f"Facture {self.id} - {self.intervention.vehicule.immatriculation}"
