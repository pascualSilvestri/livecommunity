# Generated by Django 4.2 on 2023-04-25 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('afiliado', '0006_afiliado_telefono'),
    ]

    operations = [
        migrations.AddField(
            model_name='afiliado',
            name='referenciaAfiliado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='afiliado.afiliado'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='idCliente',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]