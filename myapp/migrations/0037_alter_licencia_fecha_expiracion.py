# Generated by Django 5.0.6 on 2025-01-26 04:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0036_ruta_alter_metodo_pago_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licencia',
            name='fecha_expiracion',
            field=models.DateField(default=datetime.date(2030, 1, 25)),
        ),
    ]
