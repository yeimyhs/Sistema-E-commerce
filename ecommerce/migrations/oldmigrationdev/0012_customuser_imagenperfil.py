# Generated by Django 5.1.2 on 2024-11-29 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0011_remove_tblitem_idmarca'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='imagenperfil',
            field=models.ImageField(blank=True, null=True, upload_to='perfilUsuarioimagen/'),
        ),
    ]
