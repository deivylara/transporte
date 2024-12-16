from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.

class Stock(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    stock_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    stock_final = models.DecimalField(max_digits=10, decimal_places=2)
    descarga = models.DecimalField(max_digits=10, decimal_places=2)
    diferencias = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'grifo_stock'
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


class Turno(models.Model):
    DIA_NOCHE_CHOICES = [
        ('D', 'Día'),
        ('N', 'Noche'),
    ]
    
    nombre = models.CharField(max_length=1, choices=DIA_NOCHE_CHOICES)

    class Meta:
        db_table = 'grifo_turnos'
        verbose_name_plural = 'turnos'

    def __str__(self):
        return dict(self.DIA_NOCHE_CHOICES).get(self.nombre)
    

class Surtidor(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'grifo_surtidores'
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
        db_table = 'grifo_contadores_surtidor'
        verbose_name_plural = 'contadores por surtidor'