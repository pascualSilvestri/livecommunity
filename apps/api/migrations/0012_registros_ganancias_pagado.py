# Generated by Django 4.2.4 on 2023-08-16 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_registros_ganancias_fpa'),
    ]

    operations = [
        migrations.AddField(
            model_name='registros_ganancias',
            name='pagado',
            field=models.BooleanField(default=False),
        ),
    ]
