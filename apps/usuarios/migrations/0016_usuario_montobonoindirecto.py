# Generated by Django 4.2 on 2023-08-10 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0015_usuario_montopagar'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='montoBonoIndirecto',
            field=models.FloatField(default=0.0),
        ),
    ]
