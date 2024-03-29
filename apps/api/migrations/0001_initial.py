# Generated by Django 4.2.4 on 2023-08-12 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Relation_fpa_client',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fpa', models.CharField(max_length=50)),
                ('client', models.CharField(max_length=100)),
                ('full_name', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=50)),
                ('fecha_registro', models.DateField(null=True)),
                ('fecha_creacion', models.DateField(null=True)),
                ('fecha_verificacion', models.DateField(null=True)),
                ('status', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
