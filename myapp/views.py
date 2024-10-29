from django.http import HttpResponse
from .models import Project, UnidadTransporte, Stock, ContadorSurtidor
from django.shortcuts import render , redirect
from .forms import CreateNewProject, UnidadTransporteForm, StockForm, ContadorSurtidorFormSet
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def about(request):
    return render(request, 'about.html')

@login_required
def listar_unidades(request):
    unidades = UnidadTransporte.objects.all()
    for unidad in unidades:
        unidad.socio_display = "Sí" if unidad.socio else "No"
        unidad.responsable_display = unidad.responsable
        unidad.contacto_display = unidad.contacto
        unidad.estado_display = "ACTIVO" if unidad.estado else "SUSPENDIDO"
    return render(request, 'unidades/listar_unidades.html', {'unidades': unidades})

@login_required
def crear_unidad(request):
    if request.method == 'POST':
        form = UnidadTransporteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_unidades')
    else:
        form = UnidadTransporteForm()
    return render(request, 'unidades/crear_unidad.html', {'form': form})


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


         
         
         
         
         
@login_required
def hello(request, username):
    print(username)
    return HttpResponse("<h1>Hello %s</h1>" % username)


def exit(request):
    logout(request)
    return redirect('login')







@login_required
def projects(request):
    #projects = list(Project.objects.values())  # get all objects
    projects = Project.objects.all()
    return render(request, 'projects/projects.html',{
        'projects': projects
    })