# Generated by Django 4.2.1 on 2024-09-13 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_usuario_url_video'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='uplink',
            new_name='up_line',
        ),
    ]