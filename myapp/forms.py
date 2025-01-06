from django import forms
from .models import UnidadTransporte, controlUnidades, pagos, Licencia, tarifa
from django.forms import modelformset_factory
from datetime import date

#SECCION UNIDADES DE TRANSPORTE

class UnidadTransporteForm(forms.ModelForm):
    class Meta:
        model = UnidadTransporte
        fields = ['numero_unidad', 'socio', 'id_tarifa', 'placa', 'responsable', 'contacto', 'estado', 'vencimiento_soat', 'vencimiento_civm']
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
            'id_tarifa': 'Tarifa',
            'responsable' : 'Locador'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_tarifa'].required = False

    def clean(self):
        # Obtener datos limpios del formulario
        cleaned_data = super().clean()
        socio = cleaned_data.get('socio')
        if socio is not None:
            tarifa_asignada = tarifa.objects.filter(nombre_tarifa="PREMIUM" if socio else "STANDAR").first()
            if not tarifa_asignada:
                raise forms.ValidationError("No se encontró una tarifa válida para el socio.")
            cleaned_data['id_tarifa'] = tarifa_asignada
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        socio = self.cleaned_data.get('socio')
        instance.id_tarifa = tarifa.objects.filter(nombre_tarifa="PREMIUM" if socio else "STANDAR").first()
        if commit:
            instance.save()
        return instance
    
class editarUnidad(forms.ModelForm):
    class Meta:
        model = UnidadTransporte
        fields = ['numero_unidad', 'placa', 'socio', 'id_tarifa', 'responsable', 'contacto','estado', 'vencimiento_soat', 'vencimiento_civm']
        widgets = {
            'vencimiento_soat': forms.DateInput(attrs={'type': 'date'}),
            'vencimiento_civm': forms.DateInput(attrs={'type': 'date'}),
        }

#SECCION CONTROL DE UNIDADES

class ControlUnidadesForm(forms.ModelForm):
    class Meta:
        model = controlUnidades
        fields = ['unidad', 'vuelta']
        widgets = {
            'vuelta': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'unidad': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Obtiene el usuario de los kwargs
        super().__init__(*args, **kwargs)
        self.fields['vuelta'].required = False
        # Filtrar el campo 'unidad' para mostrar solo unidades activas o suspendidas
        self.fields['unidad'].queryset = UnidadTransporte.objects.filter(
            estado__in=[True]  # Ajusta el filtro según tus necesidades
        )

    def clean(self):
        cleaned_data = super().clean()
        unidad = cleaned_data.get('unidad')
        if unidad is not None:
            siguiente_vuelta = controlUnidades(unidad=unidad).calcular_siguiente_vuelta()
            cleaned_data['vuelta'] = siguiente_vuelta
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.usuario = self.user
        unidad = self.cleaned_data.get('unidad')
        if unidad is not None:
            siguiente_vuelta = controlUnidades(unidad=unidad).calcular_siguiente_vuelta()
            instance.vuelta = siguiente_vuelta
        if commit:
            instance.save()
        return instance

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
            'fecha_pago': forms.DateInput(attrs={'type': 'date'}),
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