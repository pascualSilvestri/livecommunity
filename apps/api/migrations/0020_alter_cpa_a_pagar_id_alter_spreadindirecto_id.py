# Generated by Django 4.2.1 on 2023-09-16 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_rename_client_spreadindirecto_fpa_child'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cpa_a_pagar',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='spreadindirecto',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
