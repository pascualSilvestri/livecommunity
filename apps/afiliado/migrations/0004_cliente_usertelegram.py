# Generated by Django 4.2 on 2023-04-20 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afiliado', '0003_cliente_alter_afiliado_idafiliado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='userTelegram',
            field=models.CharField(default='--', max_length=200),
            preserve_default=False,
        ),
    ]