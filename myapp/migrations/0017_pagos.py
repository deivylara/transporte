# Generated by Django 5.1.3 on 2024-11-17 06:27

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_metodo_pago'),
    ]

    operations = [
        migrations.CreateModel(
            name='pagos',
            fields=[
                ('id_pago', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_pago', models.DateField(default=datetime.date.today)),
                ('detalle', models.TextField(default='sin detalle', max_length=60)),
                ('id_control', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.controlunidades')),
                ('id_metodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.metodo_pago')),
                ('id_transporte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.unidadtransporte')),
            ],
            options={
                'verbose_name_plural': 'registro de pagos',
                'db_table': 'pagos',
            },
        ),
    ]
