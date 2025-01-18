from django import forms
from .models import UnidadTransporte, controlUnidades, pagos, Licencia, tarifa
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
        model = controlUnidades
        fields = ['unidad', 'vuelta']  # Asegúrate de que 'vuelta' esté incluido
        widgets = {
            'unidad': forms.Select(attrs={'class': 'form-control'}),
            # No es necesario el widget para 'vuelta' si ya se maneja en el HTML
        }


class editaControl(forms.ModelForm):
    class Meta:
        model = controlUnidades
        fields = ['unidad', 'vuelta', 'usuario']

#SECCION PAGOS

class PagoForm(forms.ModelForm):
    class Meta:
        model = pagos
        fields = ['id_transporte','id_control', 'id_metodo', 'detalle']
        labels = {
            'id_transporte': 'Unidad de Transporte',
            'id_control': 'Vuelta',
            'id_metodo': 'Método de Pago',
            'detalle': 'Detalle',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_transporte'].queryset = UnidadTransporte.objects.filter(
            estado__in=[True]  
        )

class EditarPagoForm(forms.ModelForm):
    class Meta:
        model = pagos
        fields = ['id_control', 'id_metodo', 'id_transporte', 'fecha_pago', 'detalle', 'usuario']
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date',
            'class': 'custom-date-input',
            'placeholder': 'Selecciona una fecha'
            }),
        }
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