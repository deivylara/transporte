from django import forms
from .models import UnidadTransporte, Stock, ContadorSurtidor, controlUnidades, pagos, Licencia
from django.forms import modelformset_factory
    
    

class UnidadTransporteForm(forms.ModelForm):
    class Meta:
        model = UnidadTransporte
        fields = ['numero_unidad', 'socio', 'responsable', 'contacto', 'estado', 'vencimiento_soat']
        widgets = {
            'vencimiento_soat': forms.DateInput(attrs={
                'type': 'date',  # Muestra el calendario nativo
                'class': 'form-control',  # Opcional, para aplicar estilos
            }),
        }
        


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['stock_inicial', 'descarga', 'stock_final']



class ContadorSurtidorForm(forms.ModelForm):
    class Meta:
        model = ContadorSurtidor
        fields = ['surtidor', 'contador_inicial', 'contador_final', 'fecha_hora_final']

# Define el FormSet para manejar múltiples formularios
ContadorSurtidorFormSet = modelformset_factory(
    ContadorSurtidor,
    form=ContadorSurtidorForm,
    extra=2,  # Número inicial de formularios vacíos
    can_delete=True  # Permite eliminar formularios
)

class ControlUnidadesForm(forms.ModelForm):
    class Meta:
        model = controlUnidades
        fields = ['unidad', 'vuelta']
        widgets = {
            'vuelta': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

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