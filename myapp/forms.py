from django import forms
from .models import UnidadTransporte, controlUnidades, pagos, Licencia, tarifa
from django.forms import modelformset_factory
from datetime import date

class UnidadTransporteForm(forms.ModelForm):
    class Meta:
        model = UnidadTransporte
        fields = ['numero_unidad', 'socio', 'id_tarifa', 'responsable', 'contacto', 'estado', 'vencimiento_soat']
        widgets = {
            'vencimiento_soat': forms.DateInput(attrs={
                'type': 'date',
                'class': 'custom-date-input',
                'placeholder': 'Selecciona una fecha'
            }),
            'id_tarifa': forms.Select(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'disabled': 'disabled',
            }),
        }
        labels = {
            'id_tarifa': 'Tarifa',
        }

    def clean(self):
        # Obtener datos limpios del formulario
        cleaned_data = super().clean()
        socio = cleaned_data.get('socio')

        # Verificar que socio no sea None o vacío
        if not socio:
            self.add_error('socio', "El campo 'socio' es obligatorio.")
            return cleaned_data

        # Determinar el nombre de la tarifa según el socio
        nombre_tarifa = "PREMIUM" if socio else "STANDAR"

        # Consultar el modelo tarifa para obtener el objeto correspondiente
        tarifa_obj = tarifa.objects.filter(nombre_tarifa=nombre_tarifa).first()

        if tarifa_obj:
            # Asignar la tarifa encontrada al campo id_tarifa
            cleaned_data['id_tarifa'] = tarifa_obj
        else:
            # Agregar error si no se encuentra la tarifa
            self.add_error('id_tarifa', f"No se encontró una tarifa con el nombre '{nombre_tarifa}'.")

        return cleaned_data



class ControlUnidadesForm(forms.ModelForm):
    class Meta:
        model = controlUnidades
        fields = ['unidad', 'vuelta']
        widgets = {
            'vuelta': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        unidad = kwargs.pop('unidad', None)  # Extraemos la unidad pasada como argumento
        super().__init__(*args, **kwargs)
        if unidad:  # Si se pasa la unidad, calculamos la vuelta
            ultimo_control = (
                controlUnidades.objects.filter(unidad=unidad)
                .order_by('-vuelta')
                .first()
            )
            self.fields['vuelta'].initial = (ultimo_control.vuelta + 1) if ultimo_control else 1


class PagoForm(forms.ModelForm):
    class Meta:
        model = pagos
        fields = ['id_control', 'id_metodo', 'id_transporte', 'detalle']
        labels = {
            'id_control': 'Vuelta',
            'id_metodo': 'Método de Pago',
            'id_transporte': 'Unidad de Transporte',
            'detalle': 'Detalle',
        }
        
class LicenciaForm(forms.ModelForm):
    class Meta:
        model = Licencia
        fields = ['numero_licencia', 'nombre', 'dni', 'fecha_emision', 'fecha_expiracion', 'tipo_licencia', 'numero_unidad']
        widgets = {
            'fecha_emision': forms.DateInput(attrs={
              'type': 'date',
              'class': 'custom-date-input',
              'placeholder': 'Selecciona una fecha',
            }),

            'fecha_expiracion': forms.DateInput(attrs={
              'type': 'date',
              'class': 'custom-date-input',
              'placeholder': 'Selecciona una fecha',
              
            }),  
        }