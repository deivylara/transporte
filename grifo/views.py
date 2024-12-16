from django.http import HttpResponse
from django.shortcuts import render , redirect , get_object_or_404
from .models import  Stock, ContadorSurtidor 
from .forms import StockForm, ContadorSurtidorFormSet
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.
@login_required
def grifo(request):
    return render(request, 'layouts/grifo.html')

@login_required
def listar_stock(request):
    stocks = Stock.objects.all()
    return render(request, 'stock/listar_stock.html', {'stocks': stocks})

@login_required
def crear_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_stock')
    else:
        form = StockForm()
    return render(request, 'stock/crear_stock.html', {'form': form})


@login_required       
def crear_contadores_surtidor(request):
    if request.method == 'POST':
        formset = ContadorSurtidorFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.usuario = request.user
                instance.save()
            return redirect('success_url')  # Redirige a la URL que desees
    else:
        formset = ContadorSurtidorFormSet(queryset=ContadorSurtidor.objects.none())

    return render(request, 'contadores/crear_contadores_surtidor.html', {'formset': formset})