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
                'disabled': 'disabled',  # Deshabilitar campo en el formulario
            }),
        }
        labels = {
            'id_tarifa': 'Tarifa',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_tarifa'].required = False

    def clean(self):
        # Obtener datos limpios del formulario
        cleaned_data = super().clean()
        socio = cleaned_data.get('socio')
        if socio is not None:
            # Buscar la tarifa adecuada según el socio
            tarifa_asignada = tarifa.objects.filter(nombre_tarifa="PREMIUM" if socio else "STANDAR").first()
            if not tarifa_asignada:
                raise forms.ValidationError("No se encontró una tarifa válida para el socio.")
            # Asignar automáticamente la tarifa en el cleaned_data
            cleaned_data['id_tarifa'] = tarifa_asignada
        return cleaned_data

    def save(self, commit=True):
        # Sobrescribir save para asegurarnos de que la tarifa se asigne correctamente
        instance = super().save(commit=False)
        socio = self.cleaned_data.get('socio')
        instance.id_tarifa = tarifa.objects.filter(nombre_tarifa="PREMIUM" if socio else "STANDAR").first()
        if commit:
            instance.save()
        return instance

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