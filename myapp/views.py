from django.http import HttpResponse
from .models import UnidadTransporte, Stock, ContadorSurtidor , controlUnidades, tarifa ,metodo_pago, pagos, Licencia
from django.shortcuts import render , redirect , get_object_or_404
from .forms import UnidadTransporteForm, StockForm, ContadorSurtidorFormSet, ControlUnidadesForm, PagoForm, LicenciaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def transporte(request):
    return render(request, 'transporte.html')

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
def listar_unidades(request):
    unidades = UnidadTransporte.objects.all()
    for unidad in unidades:
        unidad.socio_display = "Sí" if unidad.socio else "No"
        unidad.responsable_display = unidad.responsable
        unidad.contacto_display = unidad.contacto
        unidad.id_tarifa__nombre_tarifa_display = unidad.id_tarifa.nombre_tarifa
        unidad.estado_display = "ACTIVO" if unidad.estado else "SUSPENDIDO"
    return render(request, 'unidades/listar_unidades.html', {'unidades': unidades})

@login_required       
def listar_control_unidades(request):
    controles = controlUnidades.objects.all()
    for control in controles:
        control.unidad_display = control.unidad.numero_unidad 
        control.vuelta_display = control.vuelta
        control.fecha_vuelta_display = control.fecha_vuelta.strftime('%d/%m/%Y')
    return render(request, 'control_unidades/listar_control.html', {'controles': controles})

@login_required       
def listar_tarifas(request):
    tarifas = tarifa.objects.all()
    for tarif in tarifas:
        tarif.nombre_tarifa_display = tarif.nombre_tarifa  
        tarif.monto_display = f"S/ {float(tarif.monto):,.2f}"  # Formato de moneda
    return render(request, 'unidades/listar_tarifa.html', {'tarifas': tarifas})  
       
@login_required
def lista_metodos_pago(request):
    listar_metodos_pago = metodo_pago.objects.all()
    for metodo in listar_metodos_pago:
        metodo.id_metodo_display = metodo.id_metodo
        metodo.tipo_display = metodo.tipo
    return render(request, 'RegistrosCertificado/listar_metodos_pago.html', {'listar_metodos_pago':listar_metodos_pago})

@login_required
def listar_pagos(request):
    pagos_list = pagos.objects.select_related(
        'id_control', 
        'id_control__unidad', 
        'id_control__unidad__id_tarifa', 
        'id_metodo'
    ).all()

    for pago in pagos_list:
        # Formatear datos relacionados
        pago.vuelta_display = pago.id_control.vuelta if pago.id_control else "N/A"
        pago.numero_unidad_display = pago.id_control.unidad.numero_unidad if pago.id_control and pago.id_control.unidad else "N/A"
        pago.nombre_tarifa_display = pago.id_control.unidad.id_tarifa.nombre_tarifa if pago.id_control and pago.id_control.unidad and pago.id_control.unidad.id_tarifa else "N/A"
        pago.metodo_pago_display = pago.id_metodo.tipo if pago.id_metodo else "N/A"
        pago.fecha_pago_display = pago.fecha_pago.strftime('%d/%m/%Y') if pago.fecha_pago else "N/A"
        pago.detalle_display = pago.detalle

    return render(request, 'pagos/listar_pagos.html', {'pagos_list': pagos_list})


@login_required
def crear_control_unidad(request):
    if request.method == 'POST':
        form = ControlUnidadesForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo registro
            return redirect('listar_control_unidades')  # Redirige a la vista que lista los controles
    else:
        form = ControlUnidadesForm()
    
    return render(request, 'control_unidades/crear_control.html', {'form': form})

@login_required
def crear_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_pagos')
    else:
        form = PagoForm()

    return render(request, 'pagos/crear_pagos.html', {'form': form})

@login_required
def listar_licencias(request):
    licencias = Licencia.objects.all()
    return render(request, 'licencias/listar_licencias.html', {'licencias': licencias})

@login_required
def crear_licencias(request):
    if request.method == 'POST':
        form = LicenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_licencias')
    else:
        form = LicenciaForm()
    return render(request, 'licencias/crear_licencias.html', {'form': form})

@login_required
def editar_licencia(request, id):
    licencia = get_object_or_404(Licencia, id=id)
    
    if request.method == 'POST':
        licencia.numero_licencia = request.POST.get('numero_licencia')
        licencia.nombre = request.POST.get('nombre')
        licencia.dni = request.POST.get('dni')
        licencia.fecha_emision = request.POST.get('fecha_emision')
        licencia.fecha_expiracion = request.POST.get('fecha_expiracion')
        licencia.tipo_licencia = request.POST.get('tipo_licencia')
        licencia.numero_unidad = request.POST.get('numero_unidad')
        licencia.save()
        return redirect('listar_licencias')  # Redirigir al listado de licencias

    return render(request, 'licencias/editar_licencia.html', {'licencia': licencia}, )

@login_required
def hello(request, username):
    print(username)
    return HttpResponse("<h1>Hello %s</h1>" % username)


def exit(request):
    logout(request)
    return redirect('login')