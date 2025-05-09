# Generated by Django 5.1.7 on 2025-05-02 14:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0002_remove_client_historique_interventions'),
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipeReparation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('specialite', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Panne',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Vehicule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marque', models.CharField(max_length=100)),
                ('modele', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Intervention',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('immatriculation', models.CharField(max_length=50, unique=True)),
                ('date_debut', models.DateTimeField(auto_now_add=True)),
                ('date_fin_prevue', models.DateTimeField()),
                ('date_fin_reelle', models.DateTimeField(blank=True, null=True)),
                ('statut', models.CharField(choices=[('en_cours', 'En cours'), ('terminee', 'Terminée'), ('annulee', 'Annulée')], default='en_cours', max_length=50)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicules', to='clients.client')),
                ('equipe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='interventions', to='interventions.equipereparation')),
                ('vehicule', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interventions', to='interventions.vehicule')),
            ],
        ),
        migrations.CreateModel(
            name='HistoriqueReparation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('details', models.TextField()),
                ('date_archivage', models.DateTimeField(auto_now_add=True)),
                ('intervention', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='historique', to='interventions.intervention')),
            ],
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('montant_main_oeuvre', models.DecimalField(decimal_places=2, max_digits=15)),
                ('date_emission', models.DateTimeField(auto_now_add=True)),
                ('statut', models.CharField(choices=[('payee', 'Payée'), ('impayee', 'Imppayée')], default='impayee', max_length=50)),
                ('intervention', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='facture', to='interventions.intervention')),
            ],
        ),
        migrations.CreateModel(
            name='MaterielUtilise',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantite', models.PositiveIntegerField()),
                ('intervention', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materiels_utilises', to='interventions.intervention')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='utilisations', to='stock.stock')),
            ],
        ),
        migrations.CreateModel(
            name='LignePanne',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('date_signalement', models.DateTimeField(auto_now_add=True)),
                ('intervention', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lignes_pannes', to='interventions.intervention')),
                ('panne', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lignes_pannes', to='interventions.panne')),
            ],
        ),
    ]
