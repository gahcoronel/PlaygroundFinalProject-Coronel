# Generated by Django 5.0.1 on 2024-03-06 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_alter_articulo_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='imagen',
            field=models.ImageField(null=True, upload_to='postales'),
        ),
    ]