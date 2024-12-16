from django import forms
from .models import Stock, ContadorSurtidor
from django.forms import modelformset_factory


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