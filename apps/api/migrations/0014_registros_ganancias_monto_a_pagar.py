# Generated by Django 4.2.4 on 2023-08-18 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_registros_ganancias_spreak_direct_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='registros_ganancias',
            name='monto_a_pagar',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
