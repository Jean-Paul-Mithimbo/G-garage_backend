from django.db import models
from clients.models import Client
from ressources_humaine.models import Employe
from stock.models import Stock
from django.contrib.auth import get_user_model

# # Modèle Client
# class Client(models.Model):
#     id = models.AutoField(primary_key=True)
#     nom = models.CharField(max_length=255)
#     contact = models.CharField(max_length=255)

#     def __str__(self):
#         return self.nom

# Modèle Véhicule
class Vehicule(models.Model):
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    
    

    def __str__(self):
        return f"{self.marque} {self.modele}"

# Modèle Panne
class Panne(models.Model):
    id = models.AutoField(primary_key=True)
    nom= models.CharField(max_length=100)
    description = models.TextField()
    

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
    immatriculation = models.CharField(max_length=50, null=True, blank=True)  # Optional field for immatriculation
    client = models.ForeignKey(Client, related_name='vehicules', on_delete=models.CASCADE)
    equipe = models.ForeignKey(EquipeReparation, related_name='interventions', on_delete=models.SET_NULL, null=True)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin_prevue = models.DateTimeField()
    date_fin_reelle = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=50, choices=[('en_cours', 'En cours'), ('terminee', 'Terminée'), ('annulee', 'Annulée')], default='en_cours')

    def __str__(self):
        return f"Intervention {self.id} - {self.vehicule.marque if self.vehicule else 'Aucun véhicule'}"

# class InterventionDraft(models.Model):
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="drafts")
#     data = models.JSONField()  # Toutes les infos du brouillon (étapes, valeurs, etc.)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


class InterventionDraft(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="drafts")
    data = models.JSONField()  # Toutes les infos du brouillon (étapes, valeurs, etc.)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Brouillon #{self.id} de {self.user}"

# Modèle Ligne de Panne
class LignePanne(models.Model):
    id = models.AutoField(primary_key=True)
    intervention = models.ForeignKey(Intervention, related_name='lignes_pannes', on_delete=models.CASCADE)
    panne = models.ForeignKey(Panne, related_name='lignes_pannes', on_delete=models.CASCADE)
    description=models.TextField()
    date_signalement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Panne {self.panne.id} liée à Intervention {self.intervention.id}"

# Modèle Matériel utilisé dans une intervention
class MaterielUtilise(models.Model):
    id = models.AutoField(primary_key=True)
    intervention = models.ForeignKey(Intervention, related_name='materiels_utilises', on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, related_name='utilisations', on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()


    def save(self, *args, **kwargs):
        """Crée une sortie de stock lors de l'utilisation de matériel."""
        from stock.models import Sortie, LigneSortie
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            # Crée une sortie et une ligne de sortie pour ce matériel utilisé
            sortie = Sortie.objects.create(motif=f"Utilisation pour intervention {self.intervention.id}")
            LigneSortie.objects.create(
                sortie=sortie,
                article=self.stock.article,
                quantite=self.quantite
            )

    def delete(self, *args, **kwargs):
        """Crée une entrée de stock lors de la suppression de l'utilisation de matériel."""
        from stock.models import Entree, LigneEntree
        # On remet le stock via une entrée
        entree = Entree.objects.create(libele=f"Annulation utilisation intervention {self.intervention.id}", date_op=self.intervention.date_debut.date())
        LigneEntree.objects.create(
            entree=entree,
            article=self.stock.article,
            quantite=self.quantite,
            prix_unitaire=0,  # À adapter si besoin
            date_expiration=None
        )
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
        from stock.models import LigneEntree
        montant_materiels = 0
        for materiel in self.intervention.materiels_utilises.all():
            # Cherche la dernière entrée pour cet article
            ligne_entree = LigneEntree.objects.filter(article=materiel.stock.article).order_by('-date_entree').first()
            prix_unitaire = ligne_entree.prix_unitaire if ligne_entree else 0
            montant_materiels += materiel.quantite * prix_unitaire
        return self.montant_main_oeuvre + montant_materiels

    def __str__(self):
        return f"Facture {self.id} - {self.intervention.vehicule.immatriculation}"
