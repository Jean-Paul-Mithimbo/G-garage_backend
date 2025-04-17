# Generated by Django 5.1.7 on 2025-04-17 09:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('caracteristiques', models.JSONField(default=dict)),
            ],
        ),
        migrations.RemoveField(
            model_name='livraison',
            name='commande',
        ),
        migrations.RemoveField(
            model_name='détailcommande',
            name='commande',
        ),
        migrations.RemoveField(
            model_name='détailcommande',
            name='stock',
        ),
        migrations.RemoveField(
            model_name='retour',
            name='livraison',
        ),
        migrations.RemoveField(
            model_name='retour',
            name='stock',
        ),
        migrations.RemoveField(
            model_name='fournisseur',
            name='liste_produits',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='fournisseur',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='nom',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='reference',
        ),
        migrations.AddField(
            model_name='stock',
            name='prix_unitaire',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='fournisseur',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AddField(
            model_name='stock',
            name='article',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stock', to='stock.article'),
        ),
        migrations.DeleteModel(
            name='Commande',
        ),
        migrations.DeleteModel(
            name='DétailCommande',
        ),
        migrations.DeleteModel(
            name='Livraison',
        ),
        migrations.DeleteModel(
            name='Retour',
        ),
    ]
