# Generated by Django 4.2.4 on 2023-08-13 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_registro_archivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro_archivo',
            name='fpa',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
