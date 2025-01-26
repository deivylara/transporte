from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)

    def __str__(self): 
        return self.title + " - " + self.project.name
       
    


class tarifa(models.Model):
    id_tarifa = models.AutoField(primary_key=True)
    nombre_tarifa = models.TextField(max_length=80, default='personalizado')
    monto = models.TextField(max_length=40, default='0.00')

    class Meta:
        db_table = 'tarifa_unidades'
        verbose_name_plural = 'tarifa de unidades'
    
    def __str__(self):
        return f'Tarifa {self.nombre_tarifa } - monto {self.monto}'

class UnidadTransporte(models.Model): 
    id_transporte = models.AutoField(primary_key=True)
    numero_unidad = models.IntegerField(unique=True, null=True, blank=True)
    placa = models.CharField(max_length=8,unique=True, null=True)
    socio = models.BooleanField(default=False)
    responsable = models.TextField(max_length=20, null=True)
    contacto = models.CharField(max_length=8, null=True)
    estado = models.BooleanField(default=True)
    vencimiento_soat = models.DateField(default=date.today)
    vencimiento_civm = models.DateField(default=date.today)

    class Meta:
        db_table = 'unidades_transporte'
        verbose_name_plural = 'Unidades de Transporte'

    def __str__(self):
        return f'Unidad {self.numero_unidad}'



class ControlUnidades(models.Model):
    id_control = models.AutoField(primary_key=True)
    unidad = models.ForeignKey(UnidadTransporte, on_delete=models.CASCADE)
    vuelta = models.IntegerField(null=True, blank=True)
    fecha_vuelta = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'control_unidades'  # Esto asegura que la tabla siga con el nombre correcto
        verbose_name_plural = 'control de unidades'


    
    


class Licencia(models.Model):
    TIPO_LICENCIA_CHOICES = [
        ('allb', 'Microbuses o minibuses(allb) '),
        ('allla', 'Omnibuses urbanos(allla)'),
        ('alllb', 'Omnibuses interurbanos(alllb)'),
    ]

    numero_licencia = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=15, unique=True)
    fecha_emision = models.DateField(default=date.today)
    fecha_expiracion = models.DateField(default= date.today().replace(year=date.today().year + 5))
    tipo_licencia = models.CharField(
        max_length=60,
        choices=TIPO_LICENCIA_CHOICES,
        default='Allb', 
    ) 
    numero_unidad = models.ForeignKey(
        UnidadTransporte, 
        on_delete=models.CASCADE, 
        related_name='licencias',
        null=True,
        blank=True
        
        
    )

    class Meta:
        db_table = 'licencias'
        verbose_name = 'Licencia'
        verbose_name_plural = 'Licencias'
        ordering = ['fecha_expiracion']

    def __str__(self):
        return f"{self.numero_licencia} - {self.nombre} ({self.get_tipo_licencia_display()})"



# Modelo Ruta
class Ruta(models.Model):
    id_ruta = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'rutas'
        verbose_name_plural = 'Rutas'

    def __str__(self):
        return self.nombre

# Modelo Metodo_Pago
class Metodo_Pago(models.Model):
    id_metodo = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50)

    class Meta:
        db_table = 'metodo_pago'
        verbose_name_plural = 'Metodos de Pago'

    def __str__(self):
        return self.tipo



# Modelo PagoDiario
class PagoDiario(models.Model):
    unidad_transporte = models.ForeignKey(UnidadTransporte, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    metodo_pago = models.ForeignKey(Metodo_Pago, on_delete=models.CASCADE)
    monto_pagado = models.DecimalField(max_digits=6, decimal_places=2)
    fecha_pago = models.DateField(default=date.today)
    observaciones = models.TextField(null=True, blank=True)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    numero_vuelta = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'pagos_diarios'
        verbose_name_plural = 'Pagos Diarios'