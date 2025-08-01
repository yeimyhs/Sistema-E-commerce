# Generated by Django 5.1.2 on 2024-12-08 05:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0017_tblcarrusel_delete_tblslider_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblitem',
            name='activo',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tblitem',
            name='idmarca',
            field=models.ForeignKey(blank=True, db_column='id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ecommerce.marca'),
        ),
    ]
