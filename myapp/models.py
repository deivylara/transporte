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
    


class Stock(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    stock_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    stock_final = models.DecimalField(max_digits=10, decimal_places=2)
    descarga = models.DecimalField(max_digits=10, decimal_places=2)
    diferencias = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'stock'
        verbose_name_plural = 'stocks'

    def save(self, *args, **kwargs):
        # Calcular diferencias
        suma_inicial_descarga = self.stock_inicial + self.descarga
        self.diferencias = suma_inicial_descarga - self.stock_final
        super().save(*args, **kwargs)

    def __str__(self):
        return (f"Record at {self.timestamp} - Initial: {self.stock_inicial}, "
                f"Final: {self.stock_final}, Descarga: {self.descarga}, "
                f"Diferencias: {self.diferencias}")


class Surtidor(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'surtidores'
        verbose_name_plural = 'surtidores'

    def __str__(self):
        return self.nombre
    
    
    
class Turno(models.Model):
    DIA_NOCHE_CHOICES = [
        ('D', 'Día'),
        ('N', 'Noche'),
    ]
    
    nombre = models.CharField(max_length=1, choices=DIA_NOCHE_CHOICES)

    class Meta:
        db_table = 'turnos'
        verbose_name_plural = 'turnos'

    def __str__(self):
        return dict(self.DIA_NOCHE_CHOICES).get(self.nombre)


class Surtidor(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'surtidores'
        verbose_name_plural = 'surtidores'

    def __str__(self):
        return self.nombre


class ContadorSurtidor(models.Model):
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    surtidor = models.ForeignKey(Surtidor, on_delete=models.CASCADE)
    contador_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    contador_final = models.DecimalField(max_digits=10, decimal_places=2)
    diferencias = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_hora_inicio = models.DateTimeField(auto_now_add=True)
    fecha_hora_final = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'contadores_surtidor'
        verbose_name_plural = 'contadores por surtidor'

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
    socio = models.BooleanField(default=False)
    responsable = models.TextField(max_length=20, null=True)
    contacto = models.CharField(max_length=8, null=True)
    id_tarifa = models.ForeignKey(tarifa, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    vencimiento_soat = models.DateField(default="2024-01-01")
    

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
    
    class Meta:
        db_table = 'control_unidades'
        verbose_name_plural = 'control de unidades'

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

    numero_licencia = models.CharField(max_length=20, unique=True)  # Número único de licencia
    nombre = models.CharField(max_length=100)  # Nombre asociado a la licencia
    dni = models.CharField(max_length=15, unique=True)  # Número de DNI o identificador único
    fecha_emision = models.DateField()  # Fecha de emisión
    fecha_expiracion = models.DateField()  # Fecha de expiración
    tipo_licencia = models.CharField(
        max_length=60,
        choices=TIPO_LICENCIA_CHOICES,
        default='Allb',  # Valor predeterminado
    )  # Tipo de licencia
    numero_unidad = models.ForeignKey(
        UnidadTransporte, 
        on_delete=models.CASCADE, 
        related_name='licencias',
        null=True,
        blank=True
        
        
    )  # Relación con UnidadTransporte

    class Meta:
        db_table = 'licencias'  # Nombre personalizado para la tabla
        verbose_name = 'Licencia'
        verbose_name_plural = 'Licencias'
        ordering = ['fecha_expiracion']  # Orden predeterminado en consultas

    def __str__(self):
        return f"{self.numero_licencia} - {self.nombre} ({self.get_tipo_licencia_display()})"

