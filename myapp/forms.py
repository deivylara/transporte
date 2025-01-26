from django import forms
from .models import UnidadTransporte, ControlUnidades, Licencia, PagoDiario
from django.forms import modelformset_factory
from datetime import date

#SECCION UNIDADES DE TRANSPORTE

class UnidadTransporteForm(forms.ModelForm):
    class Meta:
        model = UnidadTransporte
        fields = ['numero_unidad', 'socio', 'placa', 'responsable', 'contacto', 'estado', 'vencimiento_soat', 'vencimiento_civm']
        widgets = {
            'vencimiento_soat': forms.DateInput(attrs={
                'type': 'date',
                'class': 'custom-date-input',
                'placeholder': 'Selecciona una fecha'
            }),
            'vencimiento_civm': forms.DateInput(attrs={
                'type': 'date',
                'class': 'custom-date-input',
                'placeholder': 'Selecciona una fecha'
            }),
            'id_tarifa': forms.Select(attrs={
                'class': 'form-control',
                'disabled': 'disabled',
            }),
        }
        labels = {
            'responsable' : 'Locador'
        }
    
class editarUnidad(forms.ModelForm):
    class Meta:
        model = UnidadTransporte
        fields = ['numero_unidad', 'placa', 'socio', 'responsable', 'contacto','estado', 'vencimiento_soat', 'vencimiento_civm']
        widgets = {
            'vencimiento_soat': forms.DateInput(attrs={'type': 'date', 
            'class': 'custom-date-input',
            'placeholder': 'Selecciona una fecha'
        }),
            'vencimiento_civm': forms.DateInput(attrs={'type': 'date',
            'class': 'custom-date-input',
            'placeholder': 'Selecciona una fecha'
        }),
        }

#SECCION CONTROL DE UNIDADES

class ControlUnidadesForm(forms.ModelForm):
    class Meta:
        model = ControlUnidades
        fields = ['unidad', 'vuelta']  # Asegúrate de que 'vuelta' esté incluido
        widgets = {
            'unidad': forms.Select(attrs={'class': 'form-control'}),
            # No es necesario el widget para 'vuelta' si ya se maneja en el HTML
        }


class editaControl(forms.ModelForm):
    class Meta:
        model = ControlUnidades
        fields = ['unidad', 'vuelta', 'usuario']


#SECCION LICENCIAS

class LicenciaForm(forms.ModelForm):
    class Meta:
        model = Licencia
        fields = ['numero_licencia', 'nombre', 'dni', 'fecha_emision', 'fecha_expiracion', 'tipo_licencia', 'numero_unidad']
        widgets = {
            'fecha_emision': forms.DateInput(attrs={
              'type': 'date',
                'class': 'custom-date-input',
                'placeholder': 'Selecciona una fecha'
            }),

            'fecha_expiracion': forms.DateInput(attrs={
              'type': 'date',
                'class': 'custom-date-input',
                'placeholder': 'Selecciona una fecha'
              
            }),  
        }



class PagoDiarioForm(forms.ModelForm):
    class Meta:
        model = PagoDiario
        fields = ['unidad_transporte', 'ruta', 'metodo_pago', 'observaciones']

    def save(self, commit=True):
        pago = super().save(commit=False)

        # Obtener información de la unidad de transporte
        unidad = pago.unidad_transporte
        ruta = pago.ruta

        # Calcular el monto a pagar
        if ruta.nombre == 'P13':
            pago.monto_pagado = 15 if unidad.socio else 20
        elif ruta.nombre == 'C13':
            pago.monto_pagado = 15

        # Determinar la vuelta más reciente
        ultima_vuelta = ControlUnidades.objects.filter(
            unidad=unidad,
            fecha_vuelta__date=pago.fecha_pago
        ).order_by('-fecha_vuelta').first()
        if ultima_vuelta:
            pago.numero_vuelta = ultima_vuelta.vuelta

        if commit:
            pago.save()
        return pago