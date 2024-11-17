from django import forms
from .models import UnidadTransporte, Stock, ContadorSurtidor, controlUnidades, pagos
from django.forms import modelformset_factory
    
    
class CreateNewProject(forms.Form):
    name = forms.CharField(label="nombre del proyecto", max_length=200)
    

class UnidadTransporteForm(forms.ModelForm):
    class Meta:
        model = UnidadTransporte
        fields = ['numero_unidad', 'socio', 'responsable', 'contacto',  'estado',]   
        


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
