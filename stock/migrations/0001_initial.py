# Generated by Django 5.1.7 on 2025-04-17 04:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fournisseur',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=255)),
                ('adresse', models.TextField()),
                ('liste_produits', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_commande', models.DateTimeField(auto_now_add=True)),
                ('statut', models.CharField(choices=[('en_attente', 'En attente'), ('expediee', 'Expédiée'), ('livree', 'Livrée'), ('annulee', 'Annulée')], default='en_attente', max_length=50)),
                ('fournisseur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commandes', to='stock.fournisseur')),
            ],
        ),
        migrations.CreateModel(
            name='Livraison',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_livraison', models.DateTimeField(blank=True, null=True)),
                ('statut', models.CharField(choices=[('en_cours', 'En cours'), ('livree', 'Livrée'), ('retournee', 'Retournée')], default='en_cours', max_length=50)),
                ('commande', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='livraison', to='stock.commande')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reference', models.CharField(max_length=100, unique=True)),
                ('nom', models.CharField(max_length=255)),
                ('quantite', models.PositiveIntegerField()),
                ('seuil_alerte', models.PositiveIntegerField(default=10)),
                ('fournisseur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='stock.fournisseur')),
            ],
        ),
        migrations.CreateModel(
            name='Retour',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantite', models.PositiveIntegerField()),
                ('raison', models.TextField()),
                ('livraison', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='retours', to='stock.livraison')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='retours', to='stock.stock')),
            ],
        ),
        migrations.CreateModel(
            name='DétailCommande',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantite', models.PositiveIntegerField()),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='stock.commande')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commandes', to='stock.stock')),
            ],
        ),
    ]
