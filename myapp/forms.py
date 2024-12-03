from django import forms
from .models import UnidadTransporte, Stock, ContadorSurtidor, controlUnidades, pagos, Licencia
from django.forms import modelformset_factory
    
    

class UnidadTransporteForm(forms.ModelForm):
    class Meta:
        model = UnidadTransporte
        fields = ['numero_unidad', 'id_tarifa', 'socio', 'responsable', 'contacto', 'estado', 'vencimiento_soat']
        widgets = {
            'vencimiento_soat': forms.DateInput(attrs={
                'type': 'date',  # Muestra el calendario nativo
                'class': 'form-control',  # Opcional, para aplicar estilos
            }),
            
            'id_tarifa': forms.TextInput(attrs={'readonly': 'readonly'})
        }
        labels ={
            'id_tarifa' :'Tarifa'
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