# Generated by Django 5.0.6 on 2025-01-16 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0032_alter_licencia_fecha_expiracion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controlunidades',
            name='vuelta',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
