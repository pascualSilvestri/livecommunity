# Generated by Django 4.2.1 on 2024-09-13 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_tokenpassword'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='url_video',
            field=models.URLField(default='https://www.youtube.com/watch?v=HgKjhFEguy'),
        ),
    ]