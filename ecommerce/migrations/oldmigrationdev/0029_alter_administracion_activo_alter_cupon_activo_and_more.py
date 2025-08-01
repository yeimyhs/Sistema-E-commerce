# Generated by Django 5.1.2 on 2024-12-18 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0028_tblitemclasevinculo_delete_tblitemclasepropiedad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administracion',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='cupon',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='marca',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='moneda',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='promocion',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tblcarrito',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tblcarrusel',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tbldetallecarrito',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tbldetallepedido',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tblimagenitem',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tblitem',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tblitemclase',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tblitemclasevinculo',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tblitemcupon',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tblitempropiedad',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tblitemrelacionado',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tblmodelo',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tblnoticia',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tblpedido',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tipocambio',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='valoracion',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]
