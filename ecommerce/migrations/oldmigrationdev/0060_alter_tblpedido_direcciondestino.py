# Generated by Django 5.1.2 on 2025-01-19 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0059_alter_tblpedido_departamento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblpedido',
            name='direcciondestino',
            field=models.TextField(blank=True, null=True),
        ),
    ]
