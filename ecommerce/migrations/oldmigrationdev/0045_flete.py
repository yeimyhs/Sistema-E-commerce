# Generated by Django 5.1.2 on 2025-01-08 15:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0044_cupon_tipocupon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flete',
            fields=[
                ('activo', models.BooleanField(default=1)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('iddepartamento', models.CharField(choices=[('01', 'Amazonas'), ('02', 'Áncash'), ('03', 'Apurímac'), ('04', 'Arequipa'), ('05', 'Ayacucho'), ('06', 'Cajamarca'), ('07', 'Callao'), ('08', 'Cusco'), ('09', 'Huancavelica'), ('10', 'Huánuco'), ('11', 'Ica'), ('12', 'Junín'), ('13', 'La Libertad'), ('14', 'Lambayeque'), ('15', 'Lima'), ('16', 'Loreto'), ('17', 'Madre de Dios'), ('18', 'Moquegua'), ('19', 'Pasco'), ('20', 'Piura'), ('21', 'Puno'), ('22', 'San Martín'), ('23', 'Tacna'), ('24', 'Tumbes'), ('25', 'Ucayali')], max_length=2, verbose_name='Departamento')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=20)),
                ('idcategoria', models.ForeignKey(db_column='idcategoria', on_delete=django.db.models.deletion.CASCADE, to='ecommerce.tblcategoria')),
            ],
            options={
                'db_table': 'Flete',
            },
        ),
    ]
