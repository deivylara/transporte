from django import forms
from .models import UnidadTransporte, controlUnidades, pagos, Licencia,tarifa
from django.forms import modelformset_factory

class UnidadTransporteForm(forms.ModelForm):
    class Meta:
        model = UnidadTransporte
        fields = ['numero_unidad', 'socio',  'id_tarifa','responsable', 'contacto', 'estado', 'vencimiento_soat']
        widgets = {
            'vencimiento_soat': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
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
        cleaned_data = super().clean()
        socio = cleaned_data.get('socio')
        if socio is not None:
            # Asignar id_tarifa basado en socio
            tarifa = tarifa.objects.filter(nombre_tarifa="PREMIUM" if socio else "STANDAR").first()
            cleaned_data['id_tarifa'] = tarifa
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