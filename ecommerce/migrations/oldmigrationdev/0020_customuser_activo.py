# Generated by Django 5.1.2 on 2024-12-08 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0019_administracion_activo_cupon_activo_marca_activo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='activo',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
