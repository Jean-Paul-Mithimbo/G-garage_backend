from django.db import models

class Client(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
 

    def __str__(self):
        return self.nom

class Devis(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, related_name='devis', on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_validite = models.DateTimeField()
    statut = models.CharField(max_length=50, choices=[('en_attente', 'En attente'), ('accepte', 'Accepté'), ('refuse', 'Refusé')])

    def __str__(self):
        return f"Devis {self.id} pour {self.client.nom}"

# class Facture(models.Model):
#     id = models.AutoField(primary_key=True)
#     client = models.ForeignKey(Client, related_name='factures', on_delete=models.CASCADE)
#     montant = models.DecimalField(max_digits=10, decimal_places=2)
#     date_creation = models.DateTimeField(auto_now_add=True)
#     date_echeance = models.DateTimeField()
#     statut = models.CharField(max_length=50, choices=[('en_attente', 'En attente'), ('payee', 'Payée'), ('en_retard', 'En retard')])

#     def __str__(self):
#         return f"Facture {self.id} pour {self.client.nom}"

# class Paiement(models.Model):
#     id = models.AutoField(primary_key=True)
#     facture = models.ForeignKey(Facture, related_name='paiements', on_delete=models.CASCADE)
#     montant = models.DecimalField(max_digits=10, decimal_places=2)
#     date_paiement = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Paiement {self.id} pour la facture {self.facture.id}"

class Abonnement(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, related_name='abonnements', on_delete=models.CASCADE)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField()
    type_abonnement = models.CharField(max_length=100)

    def __str__(self):
        return f"Abonnement {self.id} pour {self.client.nom}"

class Fidélité(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, related_name='fidélites', on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    date_dernier_point = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Fidélité de {self.client.nom} avec {self.points} points"

