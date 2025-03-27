from django.db import models

# Modèle Client
class Client(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)

    def __str__(self):
        return self.nom

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
    vehicule = models.ForeignKey(Vehicule, related_name='pannes', on_delete=models.CASCADE)
    description = models.TextField()
    date_signalement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Panne {self.id} - {self.vehicule.immatriculation}"

# Modèle Équipe de Réparation
class EquipeReparation(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nom

# Modèle Intervention
class Intervention(models.Model):
    id = models.AutoField(primary_key=True)
    panne = models.ForeignKey(Panne, related_name='interventions', on_delete=models.CASCADE)
    equipe = models.ForeignKey(EquipeReparation, related_name='interventions', on_delete=models.SET_NULL, null=True)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin_prevue = models.DateTimeField()
    date_fin_reelle = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=50, choices=[('en_cours', 'En cours'), ('terminee', 'Terminée'), ('annulee', 'Annulée')], default='en_cours')

    def __str__(self):
        return f"Intervention {self.id} - {self.panne.vehicule.immatriculation}"

# Modèle Historique des réparations
class HistoriqueReparation(models.Model):
    id = models.AutoField(primary_key=True)
    intervention = models.OneToOneField(Intervention, related_name='historique', on_delete=models.CASCADE)
    details = models.TextField()
    date_archivage = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Historique de {self.intervention.panne.vehicule.immatriculation}"
