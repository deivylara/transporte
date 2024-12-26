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
    
class metodo_pago(models.Model):
    id_metodo = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50)

    class Meta:
        db_table = 'metodo_pago'
        verbose_name_plural = 'metodos de pago'

    def __str__(self):
        return f' {self.tipo}'

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
    id_tarifa = models.ForeignKey(tarifa, on_delete=models.CASCADE, default=True)
    estado = models.BooleanField(default=True)
    vencimiento_soat = models.DateField(default=date.today)
    vencimiento_civm = models.DateField(default=date.today)

    class Meta:
        db_table = 'unidades_transporte'
        verbose_name_plural = 'Unidades de Transporte'

    def __str__(self):
        return f'Unidad {self.numero_unidad}'

class controlUnidades(models.Model):
    id_control = models.AutoField(primary_key=True)
    unidad = models.ForeignKey(UnidadTransporte, on_delete=models.CASCADE)
    vuelta = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_vuelta = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'control_unidades'
        verbose_name_plural = 'control de unidades'

    def calcular_siguiente_vuelta(self):
        ultimo_control = (
            controlUnidades.objects.filter(unidad=self.unidad)
            .order_by('-vuelta')
            .first()
        )
        return (ultimo_control.vuelta + 1) if ultimo_control else 1

    def save(self, *args, **kwargs):
        if not self.pk:
            self.vuelta = self.calcular_siguiente_vuelta()
        if not self.usuario:
            from django.contrib.auth import get_user_model
            self.usuario = get_user_model().objects.get(id=kwargs.get('user_id'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Control {self.id_control} - Unidad {self.unidad.numero_unidad} - Vuelta {self.vuelta}'
    
class pagos(models.Model):
    id_pago = models.AutoField(primary_key=True)
    id_control = models.ForeignKey(controlUnidades, on_delete=models.CASCADE)
    id_metodo = models.ForeignKey(metodo_pago, on_delete=models.CASCADE)
    id_transporte = models.ForeignKey(UnidadTransporte, on_delete=models.CASCADE)
    fecha_pago = models.DateField(default=date.today)
    detalle = models.TextField(max_length=60, default='sin detalle')

    class Meta:
        db_table = 'pagos'
        verbose_name_plural = 'registro de pagos'
    
    def __str__(self):
        return f'pago {self.id_registro} - unidad {self.id_transporte.numero_unidad}'
    def formatted_fecha_pago(self):
        return self.fecha_pago.strftime(format='%d/%m/%Y')
    


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

