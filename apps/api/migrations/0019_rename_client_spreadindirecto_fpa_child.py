# Generated by Django 4.2.1 on 2023-09-16 01:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_spreadindirecto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spreadindirecto',
            old_name='client',
            new_name='fpa_child',
        ),
    ]
