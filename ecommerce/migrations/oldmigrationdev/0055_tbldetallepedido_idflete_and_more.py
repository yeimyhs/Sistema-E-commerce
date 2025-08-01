# Generated by Django 5.1.2 on 2025-01-18 05:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0054_tblsede_linkmaps'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbldetallepedido',
            name='idflete',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ecommerce.flete'),
        ),
        migrations.AddField(
            model_name='tbldetallepedido',
            name='preciorebajado',
            field=models.FloatField(default=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tbldetallepedido',
            name='preciototal',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='tbldetallepedido',
            name='preciunitario',
            field=models.FloatField(),
        ),
    ]
