# Generated by Django 5.1.2 on 2024-12-21 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0037_alter_tipocambio_tipocambio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administracion',
            name='nombreempresa',
            field=models.CharField(max_length=128),
        ),
    ]
