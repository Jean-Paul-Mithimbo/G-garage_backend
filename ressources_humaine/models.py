from django.db import models

# Create your models here.
#  Modèle des employés
class Employe(models.Model):
    POSTE_CHOICES = [
        ('Mécanicien', 'Mécanicien'),
        ('Réceptionniste', 'Réceptionniste'),
        ('Comptable', 'Comptable'),
        ('Chef d’atelier', 'Chef d’atelier'),
    ]
    
    STATUT_CHOICES = [
        ('Actif', 'Actif'),
        ('Suspendu', 'Suspendu'),
        ('Licencié', 'Licencié'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    poste = models.CharField(max_length=50, choices=POSTE_CHOICES)
    salaire_base = models.DecimalField(max_digits=10, decimal_places=2)
    contact = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_embauche = models.DateField()
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='Actif')

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.poste}"

# 🔹 2. Modèle des contrats
class Contrat(models.Model):
    TYPE_CONTRAT_CHOICES = [
        ('CDI', 'CDI'),
        ('CDD', 'CDD'),
        ('Stage', 'Stage'),
    ]
    
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    type_contrat = models.CharField(max_length=50, choices=TYPE_CONTRAT_CHOICES)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    salaire = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=50, choices=[('En cours', 'En cours'), ('Terminé', 'Terminé'), ('Résilié', 'Résilié')])

    def __str__(self):
        return f"Contrat {self.type_contrat} - {self.employe.nom} {self.employe.prenom}"

# 🔹 3. Modèle du planning des employés
class Planning(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    jour = models.CharField(max_length=10, choices=[
        ('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi'),
        ('Dimanche', 'Dimanche'),
    ])
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    def __str__(self):
        return f"{self.employe.nom} {self.employe.prenom} - {self.jour}: {self.heure_debut} à {self.heure_fin}"

# 🔹 4. Modèle des congés
class Conge(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    motif = models.TextField()
    statut = models.CharField(max_length=50, choices=[
        ('En attente', 'En attente'),
        ('Approuvé', 'Approuvé'),
        ('Refusé', 'Refusé'),
    ], default='En attente')

    def __str__(self):
        return f"Congé {self.employe.nom} {self.employe.prenom} - {self.date_debut} à {self.date_fin}"

# 🔹 5. Modèle des paiements
class Paiement(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    mois = models.CharField(max_length=20, choices=[
        ('Janvier', 'Janvier'), ('Février', 'Février'), ('Mars', 'Mars'),
        ('Avril', 'Avril'), ('Mai', 'Mai'), ('Juin', 'Juin'),
        ('Juillet', 'Juillet'), ('Août', 'Août'), ('Septembre', 'Septembre'),
        ('Octobre', 'Octobre'), ('Novembre', 'Novembre'), ('Décembre', 'Décembre'),
    ])
    annee = models.IntegerField()
    salaire_net = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Paiement {self.employe.nom} - {self.mois} {self.annee}"