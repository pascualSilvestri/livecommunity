# Generated by Django 4.2.4 on 2023-08-14 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_registros_ganancias'),
    ]

    operations = [
        migrations.AddField(
            model_name='registros_ganancias',
            name='fpa',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]