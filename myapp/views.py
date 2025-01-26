from django.http import HttpResponse
from .models import UnidadTransporte, ControlUnidades, tarifa , Metodo_Pago, Licencia, PagoDiario
from django.shortcuts import render , redirect , get_object_or_404
from .forms import UnidadTransporteForm, ControlUnidadesForm, PagoDiarioForm, LicenciaForm, editarUnidad, editaControl
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import xlsxwriter
from django.contrib import messages
from io import BytesIO
from datetime import datetime
from django.utils.timezone import now
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Max
from django.contrib.auth.models import User
from datetime import date
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
    
#SECCION UNIDADES DE TRANSPORTE

@login_required
def listar_unidades(request):
    numero_unidad = request.GET.get('numero_unidad', '').strip()
    socio = request.GET.get('socio', '').strip()
    placa = request.GET.get('placa', '').strip()
    responsable = request.GET.get('responsable','').strip()
    contacto = request.GET.get('contacto','').strip()
    estado = request.GET.get('estado', '').strip()

    if numero_unidad:
        unidades = UnidadTransporte.objects.filter(numero_unidad__icontains=numero_unidad)
    elif socio:
        unidades = UnidadTransporte.objects.filter(socio=True if socio.lower() == 'si' else False)
    elif placa:
        unidad = UnidadTransporte.objects.filter(placa__icontains=placa)
    elif responsable:
        unidades = UnidadTransporte.objects.filter(responsable__icontains=responsable)
    elif contacto:
        unidades = UnidadTransporte.objects.filter(contacto__icontains=contacto)
    elif estado:
        unidades = UnidadTransporte.objects.filter(estado=True if estado.lower() == 'activo' else False)
        
    else:
        unidades = UnidadTransporte.objects.all()

    for unidad in unidades:
        unidad.socio_display = "Sí" if unidad.socio else "No"
        unidad.placa_display = unidad.placa
        unidad.responsable_display = unidad.responsable
        unidad.contacto_display = unidad.contacto
        unidad.estado_display = "ACTIVO" if unidad.estado else "SUSPENDIDO"
    
    return render(request, 'unidades/listar_unidades.html', {
        'unidades': unidades,
        'numero_unidad': numero_unidad,
        'socio': socio,
        'placa': placa,
        'responsable': responsable,
        'contacto': contacto,
        'tarifa': tarifa,
        'estado': estado,
    })

@login_required
def editar_unidad(request, id_transporte):
    unidad = get_object_or_404(UnidadTransporte, id_transporte=id_transporte)
    if request.method == 'POST':
        form = editarUnidad(request.POST, instance=unidad)
        if form.is_valid():
            form.save()
            return redirect('listar_unidades')
    else:
        form = editarUnidad(instance=unidad)
    return render(request, 'unidades/editar_unidad.html', {'form': form, 'unidad': unidad})


@login_required       
def exportar_unidades_excel(request):
    # Obtén y valida los parámetros de entrada
    numero_unidad = request.GET.get('numero_unidad', '').strip()
    socio = request.GET.get('socio', '').strip().lower()
    placa = request.GET.get('placa', '').strip()
    responsable = request.GET.get('responsable', '').strip()
    contacto = request.GET.get('contacto', '').strip()
    estado = request.GET.get('estado', '').strip().lower()

    # Validación de valores específicos
    socio = socio if socio in ['si', 'no'] else ''
    estado = estado if estado in ['activo', 'suspendido'] else ''

    # Construcción de filtros dinámicos
    filters = {}
    if numero_unidad:
        filters['numero_unidad__icontains'] = numero_unidad
    if socio:
        filters['socio'] = socio == 'si'
    if placa:
        filters['placa__icontains'] = placa
    if responsable:
        filters['responsable__icontains'] = responsable
    if contacto:
        filters['contacto__icontains'] = contacto
    if estado:
        filters['estado'] = estado == 'activo'

    # Obtén las unidades según los filtros o todos los registros si no hay filtros
    unidades = UnidadTransporte.objects.filter(**filters) if filters else UnidadTransporte.objects.all()

    # Configura la respuesta HTTP para un archivo Excel
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Unidades")

    # Formatos del Excel
    title_format = workbook.add_format({
        'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter',
        'bg_color': '#4F81BD', 'font_color': 'white', 'border': 1
    })
    header_format = workbook.add_format({
        'bold': True, 'bg_color': '#D9E1F2', 'border': 1,
        'align': 'center', 'valign': 'vcenter'
    })
    cell_format = workbook.add_format({
        'border': 1, 'align': 'left', 'valign': 'vcenter'
    })

    # Define encabezados y anchos de columnas
    headers = ['Número Unidad', 'Socio', 'Placa', 'Responsable', 'Contacto', 'Estado', 'Vencimiento SOAT', 'Vencimiento CIVM']
    column_widths = [len(header) for header in headers]

    # Título del reporte
    worksheet.merge_range(0, 0, 0, len(headers) - 1, "Reporte Unidades de Transporte", title_format)

    # Encabezados
    for col_num, header in enumerate(headers):
        worksheet.write(1, col_num, header, header_format)

    # Escribir datos y ajustar anchos de columna
    for row_num, unidad in enumerate(unidades, start=2):
        data = [
            unidad.numero_unidad,
            "Sí" if unidad.socio else "No",
            unidad.placa,
            unidad.responsable,
            unidad.contacto,
            "ACTIVO" if unidad.estado else "SUSPENDIDO",
            unidad.vencimiento_soat.strftime('%Y-%m-%d') if unidad.vencimiento_soat else "",
            unidad.vencimiento_civm.strftime('%Y-%m-%d') if unidad.vencimiento_civm else ""
        ]
        for col_num, value in enumerate(data):
            worksheet.write(row_num, col_num, value, cell_format)
            if value:
                column_widths[col_num] = max(column_widths[col_num], len(str(value)))

    # Ajustar anchos de columna
    for col_num, width in enumerate(column_widths):
        worksheet.set_column(col_num, col_num, width + 2)

    # Autofiltro
    worksheet.autofilter(1, 0, len(unidades) + 1, len(headers) - 1)

    # Cierra el workbook y genera la respuesta
    workbook.close()
    output.seek(0)

    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Reporte_unidades.xlsx"'
    return response


# SECCION CONTROL UNIDADES

@login_required       
def listar_control_unidades(request):
    numero_control = request.GET.get('numero_control', '').strip()
    numero_unidad = request.GET.get('numero_unidad', '').strip()
    vuelta = request.GET.get('vuelta', '').strip()
    date_filterp_desde = request.GET.get('date_filterp_desde', '').strip()
    date_filterp_hasta = request.GET.get('date_filterp_hasta', '').strip()
    usuario = request.GET.get('usuario', '').strip()

    # Fecha actual como predeterminada
    today = datetime.now().date()
    if not date_filterp_desde:
        date_filterp_desde = today.strftime('%Y-%m-%d')
    if not date_filterp_hasta:
        date_filterp_hasta = today.strftime('%Y-%m-%d')

    controles = ControlUnidades.objects.all()

    # Filtros dinámicos
    if numero_control:
        controles = controles.filter(numero_control__icontains=numero_control)
    if numero_unidad:
        controles = controles.filter(unidad__numero_unidad__icontains=numero_unidad)
    if vuelta:
        controles = controles.filter(vuelta__icontains=vuelta)
    if usuario:
        controles = controles.filter(usuario__icontains=usuario)
    if date_filterp_desde and date_filterp_hasta:
        try:
            date_from = datetime.strptime(date_filterp_desde, '%Y-%m-%d').date()
            date_to = datetime.strptime(date_filterp_hasta, '%Y-%m-%d').date()
            controles = controles.filter(fecha_vuelta__date__gte=date_from, fecha_vuelta__date__lte=date_to)
        except ValueError:
            pass
      # Ordenar los registros por fecha (descendente) para que el más reciente se muestre primero
    controles = controles.order_by('-fecha_vuelta')  # Este es el cambio
    # Preparar datos adicionales para el template
    for control in controles:
        control.unidad_display = control.unidad.numero_unidad
        control.vuelta_display = control.vuelta
        control.fecha_vuelta_display = control.fecha_vuelta.strftime('%d/%m/%Y')
        control.usuario_display = control.usuario

    return render(request, 'control_unidades/listar_control.html', {
        'controles': controles,
        'numero_control': numero_control,
        'numero_unidad': numero_unidad,
        'vuelta': vuelta,
        'date_filterp_desde': date_filterp_desde,
        'date_filterp_hasta': date_filterp_hasta,
        'usuario': usuario,
    })


@login_required
def crear_control_unidad(request):
    if request.method == 'POST':
        form = ControlUnidadesForm(request.POST)
        if form.is_valid():
            control = form.save(commit=False)
            control.usuario = request.user

            # Asignamos la vuelta actual al campo `vuelta`
            vuelta_actual = request.POST.get('vuelta_actual')
            if vuelta_actual:
                control.vuelta = vuelta_actual  # Asignamos el valor de vuelta

            control.save()
            return redirect('listar_control_unidades')
    else:
        form = ControlUnidadesForm()

    vuelta_actual = None
    unidad_id = request.GET.get('unidad_id')
    if unidad_id:
        try:
            unidad = UnidadTransporte.objects.get(pk=unidad_id)
            ultimo_control = (
                ControlUnidades.objects.filter(unidad=unidad)
                .order_by('-fecha_vuelta')
                .first()
            )
            vuelta_actual = (ultimo_control.vuelta + 1) if ultimo_control else 1
        except UnidadTransporte.DoesNotExist:
            pass

    return render(
        request,
        'control_unidades/crear_control.html',
        {'form': form, 'vuelta_actual': vuelta_actual or 1},
    )

    







def obtener_vuelta_actual(request, unidad_id):
    try:
        # Usamos el campo 'id_transporte' para obtener la unidad
        unidad = UnidadTransporte.objects.get(id_transporte=unidad_id)
        fecha_actual = now().date()
        
        # Contamos el número de registros de la unidad para ese día
        vuelta_actual = ControlUnidades.objects.filter(
            unidad=unidad,
            fecha_vuelta__date=fecha_actual
        ).count() + 1  # El +1 es para contar la vuelta actual
        
        return JsonResponse({'vuelta_actual': vuelta_actual})
    
    except UnidadTransporte.DoesNotExist:
        return JsonResponse({'error': 'Unidad no encontrada'}, status=404)


@login_required       
def editar_control_unidad(request, id_control):
    control = get_object_or_404(ControlUnidades, id_control=id_control)
    if request.method == 'POST':
        form = editaControl(request.POST, instance=control)
        if form.is_valid():
            form.save()
            return redirect('listar_control_unidades')
    else:
        form = editaControl(instance=control)
    return render(request, 'control_unidades/editar_control.html', {'form': form, 'control': control})


#SECCION TARIFAS

@login_required       
def listar_tarifas(request):
    tarifas = tarifa.objects.all()
    for tarif in tarifas:
        tarif.nombre_tarifa_display = tarif.nombre_tarifa  
        tarif.monto_display = f"S/ {float(tarif.monto):,.2f}"
    return render(request, 'unidades/listar_tarifa.html', {'tarifas': tarifas}) 

#SECCION METODOS DE PAGO
       
@login_required
def lista_metodos_pago(request):
    listar_metodos_pago = Metodo_Pago.objects.all()
    for metodo in listar_metodos_pago:
        metodo.id_metodo_display = metodo.id_metodo
        metodo.tipo_display = metodo.tipo
    return render(request, 'RegistrosCertificado/listar_metodos_pago.html', {'listar_metodos_pago':listar_metodos_pago})

# SECCION PAGOS

def listar_pagos(request):
    # Filtros
    id = request.GET.get('id', '').strip()
    vuelta = request.GET.get('vuelta', '').strip()
    numero_unidad = request.GET.get('numero_unidad', '').strip()
    metodo_pago = request.GET.get('metodo_pago', '').strip()
    date_filterp_desde = request.GET.get('date_filterp_desde', date.today().strftime('%Y-%m-%d'))
    date_filterp_hasta = request.GET.get('date_filterp_hasta', date.today().strftime('%Y-%m-%d'))
    detalle = request.GET.get('detalle', '').strip()
    usuario = request.GET.get('usuario', '').strip()

    # Consulta base
    pagos_list = PagoDiario.objects.select_related(
        'unidad_transporte',  
        'ruta',  
        'metodo_pago',  
        'registrado_por'  
    ).all()

    # Aplicar filtros
    if id:
        pagos_list = pagos_list.filter(id__icontains=id)
    if vuelta:
        pagos_list = pagos_list.filter(numero_vuelta__icontains=vuelta)
    if numero_unidad:
        pagos_list = pagos_list.filter(unidad_transporte__numero_unidad__icontains=numero_unidad)
    if metodo_pago:
        pagos_list = pagos_list.filter(metodo_pago__tipo__icontains=metodo_pago)
    if detalle:
        pagos_list = pagos_list.filter(observaciones__icontains=detalle)
    if usuario:
        pagos_list = pagos_list.filter(registrado_por__username__icontains=usuario)

    # Filtro por rango de fechas
    if date_filterp_desde and date_filterp_hasta:
        try:
            pagos_list = pagos_list.filter(
                fecha_pago__range=[date_filterp_desde, date_filterp_hasta]
            )
        except ValueError:
            pass

    # Agregar datos relacionados
    for pago in pagos_list:
        pago.vuelta_display = pago.numero_vuelta if pago.numero_vuelta else "N/A"
        pago.numero_unidad_display = pago.unidad_transporte.numero_unidad if pago.unidad_transporte else "N/A"
        pago.metodo_pago_display = pago.metodo_pago.tipo if pago.metodo_pago else "N/A"
        pago.detalle_display = pago.observaciones if pago.observaciones else "N/A"
        pago.usuario_display = pago.registrado_por.username if pago.registrado_por else "N/A"
        pago.fecha_pago_display = pago.fecha_pago.strftime('%d/%m/%Y') if pago.fecha_pago else "N/A"
        pago.ruta_display = pago.ruta.nombre if pago.ruta else "N/A"
        pago.monto_pagado_display = pago.monto_pagado if pago.monto_pagado else "N/A"  # Nueva columna

    return render(request, 'pagos/listar_pagos.html', {
        'pagos_list': pagos_list,
        'id': id,
        'vuelta': vuelta,
        'numero_unidad': numero_unidad,
        'metodo_pago': metodo_pago,
        'date_filterp_desde': date_filterp_desde,
        'date_filterp_hasta': date_filterp_hasta,
        'detalle': detalle,
        'usuario': usuario,
        'today': date.today().strftime('%Y-%m-%d'),
    })









@login_required
def crear_pago(request):
    if request.method == 'POST':
        form = PagoDiarioForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.registrado_por = request.user
            pago.save()
            return redirect('listar_pagos')
    else:
        form = PagoDiarioForm()
    return render(request, 'pagos/crear_pagos.html', {'form': form})





# SECCION LICENCIAS

@login_required
def listar_licencias(request):
    numero_licencia = request.GET.get('numero_licencia', '').strip()
    nombre = request.GET.get('nombre', '').strip()
    dni = request.GET.get('dni', '').strip()
    tipo_licencia = request.GET.get('tipo_licencia', '').strip()
    date_filterp = request.GET.get('date_filterp', '').strip()

    licencias = Licencia.objects.all()
    if numero_licencia:
        licencias = licencias.filter(numero_licencia__icontains=numero_licencia)
    elif nombre:
        licencias = licencias.filter(nombre__icontains=nombre)
    elif dni:
        licencias = licencias.filter(dni__icontains=dni)
    elif tipo_licencia:
        licencias = licencias.filter(tipo_licencia__icontains=tipo_licencia)
    if date_filterp:
        try:
            month, year = map(int, date_filterp.split('/'))
            licencias = licencias.filter(fecha_expiracion__month=month, fecha_expiracion__year=year)
        except ValueError:
            pass
    else:
        licencias = Licencia.objects.all()

    return render(request, 'licencias/listar_licencias.html', {
        'licencias': licencias,
        'numero_licencia': numero_licencia,
        'nombre': nombre,
        'dni': dni,
        'tipo_licencia': tipo_licencia,
        'date_filterp': date_filterp,
    })
    
def exportar_licencias_excel(request):
    numero_licencia = request.GET.get('numero_licencia', '').strip()
    nombre = request.GET.get('nombre', '').strip()
    dni = request.GET.get('dni', '').strip()
    tipo_licencia = request.GET.get('tipo_licencia', '').strip()
    date_filterp = request.GET.get('date_filterp', '').strip()

    licencias = Licencia.objects.all()
    if numero_licencia:
        licencias = licencias.filter(numero_licencia__icontains=numero_licencia)
    if nombre:
        licencias = licencias.filter(nombre__icontains=nombre)
    if dni:
        licencias = licencias.filter(dni__icontains=dni)
    if tipo_licencia:
        licencias = licencias.filter(tipo_licencia__icontains=tipo_licencia)
    if date_filterp:
        try:
            month, year = map(int, date_filterp.split('/'))
            licencias = licencias.filter(fecha_expiracion__month=month, fecha_expiracion__year=year)
        except ValueError:
            pass

    # Crear un archivo Excel en memoria
    output = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    output['Content-Disposition'] = 'attachment; filename="Reporte-licencias.xlsx"'

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Formatos
    title_format = workbook.add_format({
        'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter',
        'bg_color': '#4F81BD', 'font_color': 'white', 'border': 1
    })
    header_format = workbook.add_format({
        'bold': True, 'bg_color': '#D9E1F2', 'border': 1,
        'align': 'center', 'valign': 'vcenter'
    })
    cell_format = workbook.add_format({
        'border': 1, 'align': 'left', 'valign': 'vcenter'
    })

    # Encabezados
    headers = ['Número de Licencia', 'Nombre', 'DNI', 'Tipo de Licencia', 'Fecha de Expiración']

    # Título del reporte
    worksheet.merge_range(0, 0, 0, len(headers) - 1, "Reporte de Licencias", title_format)

    # Escribir encabezados
    for col_num, header in enumerate(headers):
        worksheet.write(1, col_num, header, header_format)

    # Agregar datos
    for row_num, licencia in enumerate(licencias, start=2):
        worksheet.write(row_num, 0, licencia.numero_licencia, cell_format)
        worksheet.write(row_num, 1, licencia.nombre, cell_format)
        worksheet.write(row_num, 2, licencia.dni, cell_format)
        worksheet.write(row_num, 3, licencia.tipo_licencia, cell_format)
        worksheet.write(row_num, 4, licencia.fecha_expiracion.strftime('%d/%m/%Y') if licencia.fecha_expiracion else '', cell_format)

    # Aplicar autofiltro
    worksheet.autofilter(1, 0, row_num, len(headers) - 1)

    # Ajustar ancho de columnas
    column_widths = [20, 30, 15, 25, 20]
    for i, width in enumerate(column_widths):
        worksheet.set_column(i, i, width)

    workbook.close()
    return output





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
        return redirect('listar_licencias')

    return render(request, 'licencias/editar_licencia.html', {'licencia': licencia}, )

@login_required
def hello(request, username):
    print(username)
    return HttpResponse("<h1>Hello %s</h1>" % username)


def exit(request):
    logout(request)
    return redirect('login')