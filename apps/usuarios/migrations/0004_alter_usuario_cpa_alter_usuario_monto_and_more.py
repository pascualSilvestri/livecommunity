# Generated by Django 4.2 on 2023-07-25 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_usuario_cpa_usuario_monto_usuario_retiros'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='cpa',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='monto',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='retiros',
            field=models.FloatField(default=0.0),
        ),
    ]