# Generated by Django 5.1.2 on 2025-01-12 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0045_flete'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblpedido',
            name='apellidos',
            field=models.CharField(default='apellido', max_length=100, verbose_name='Apellido Materno'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tblpedido',
            name='celular',
            field=models.CharField(default='123456789', max_length=20, verbose_name='Celular o Teléfono'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tblpedido',
            name='email',
            field=models.EmailField(default='yhs@gmail.com', max_length=254, verbose_name='Correo Electrónico'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tblpedido',
            name='nombre',
            field=models.CharField(default='nombre', max_length=100, verbose_name='Nombre'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tblpedido',
            name='nroid',
            field=models.BigIntegerField(default=72222222),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tblpedido',
            name='tipoid',
            field=models.CharField(choices=[('DNI', 'DNI'), ('RUC', 'RUC')], default='DNI', max_length=25),
            preserve_default=False,
        ),
    ]
