# Generated by Django 4.2 on 2023-07-29 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0008_bonocpa_usuario_havebono'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='cpaIndirecto',
            field=models.IntegerField(default=0),
        ),
    ]
