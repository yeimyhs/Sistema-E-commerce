# Generated by Django 5.1.2 on 2025-02-05 20:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0063_alter_tblitem_descripcion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblitemclasevinculo',
            name='idclase',
            field=models.ForeignKey(db_column='idclase', on_delete=django.db.models.deletion.CASCADE, related_name='vinculos', to='ecommerce.tblitemclase'),
        ),
    ]
