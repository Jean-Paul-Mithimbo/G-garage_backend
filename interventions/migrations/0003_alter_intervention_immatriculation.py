# Generated by Django 5.1.7 on 2025-06-29 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interventions', '0002_interventiondraft'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intervention',
            name='immatriculation',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
