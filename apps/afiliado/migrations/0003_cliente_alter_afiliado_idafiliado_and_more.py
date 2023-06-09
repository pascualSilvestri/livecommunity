# Generated by Django 4.2 on 2023-04-20 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afiliado', '0002_rename_cliente_afiliado_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('apellido', models.CharField(max_length=200)),
                ('correo', models.EmailField(max_length=254)),
                ('telefono', models.IntegerField()),
                ('comprobante', models.ImageField(upload_to='comprobante')),
                ('idAfiliado', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='afiliado',
            name='idAfiliado',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='afiliado',
            name='nombre',
            field=models.CharField(max_length=200),
        ),
    ]
