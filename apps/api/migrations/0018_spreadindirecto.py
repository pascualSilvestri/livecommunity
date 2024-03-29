# Generated by Django 4.2.1 on 2023-09-16 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_rename_fecha_first_trade_registros_ganancias_fecha_operacion_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpreadIndirecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateField(auto_created=True)),
                ('monto', models.FloatField()),
                ('client', models.CharField(max_length=50)),
                ('fpa', models.CharField(max_length=50)),
                ('pagado', models.BooleanField(default=False)),
            ],
        ),
    ]
