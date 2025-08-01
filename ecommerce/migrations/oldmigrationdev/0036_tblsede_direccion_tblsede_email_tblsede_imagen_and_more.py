# Generated by Django 5.1.2 on 2024-12-19 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0035_tblreclamacion_comentario_tblreclamacion_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblsede',
            name='direccion',
            field=models.TextField(default='direccion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tblsede',
            name='email',
            field=models.EmailField(default='yh@gmail.com', max_length=254, verbose_name='Correo Electrónico'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tblsede',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='imagenessede/'),
        ),
        migrations.AddField(
            model_name='tblsede',
            name='telefono',
            field=models.CharField(default='987456321', max_length=20, verbose_name='Celular o Teléfono'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tblcategoria',
            name='imagen',
            field=models.FileField(blank=True, null=True, upload_to='iconoProiedad/'),
        ),
    ]
