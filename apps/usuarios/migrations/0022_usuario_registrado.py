# Generated by Django 4.2.4 on 2023-08-15 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0021_usuario_monto_directo'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='registrado',
            field=models.BooleanField(default=False),
        ),
    ]
