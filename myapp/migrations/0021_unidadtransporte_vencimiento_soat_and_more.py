# Generated by Django 5.0.6 on 2024-11-27 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_licencia_numero_unidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='unidadtransporte',
            name='vencimiento_soat',
            field=models.DateField(default='2024-01-01'),
        ),
        migrations.AlterField(
            model_name='licencia',
            name='numero_licencia',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
