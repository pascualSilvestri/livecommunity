# Generated by Django 4.2.4 on 2023-08-17 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0025_remove_usuario_cpa_remove_usuario_cpaindirecto_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Montos',
            new_name='Cuenta',
        ),
    ]