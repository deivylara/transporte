from django.http import HttpResponse
from .models import UnidadTransporte, controlUnidades, tarifa ,metodo_pago, pagos, Licencia
from django.shortcuts import render , redirect , get_object_or_404
from .forms import UnidadTransporteForm, ControlUnidadesForm, PagoForm, LicenciaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
import xlsxwriter
from io import BytesIO
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
def listar_unidades(request):
    numero_unidad = request.GET.get('numero_unidad', '').strip()
    socio = request.GET.get('socio', '').strip()
    placa = request.GET.get('placa', '').strip()
    responsable = request.GET.get('responsable','').strip()
    contacto = request.GET.get('contacto','').strip()
    tarifa = request.GET.get('tarifa','').strip()
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
    elif tarifa:
        unidades = UnidadTransporte.objects.filter(id_tarifa__nombre_tarifa__icontains=tarifa)
    elif estado:
        unidades = UnidadTransporte.objects.filter(estado=True if estado.lower() == 'activo' else False)
        
    else:
        unidades = UnidadTransporte.objects.all()

    for unidad in unidades:
        unidad.socio_display = "Sí" if unidad.socio else "No"
        unidad.placa_display = unidad.placa
        unidad.responsable_display = unidad.responsable
        unidad.contacto_display = unidad.contacto
        unidad.id_tarifa__nombre_tarifa_display = unidad.id_tarifa.nombre_tarifa
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




def exportar_unidades_excel(request):
    # Obtén y valida los parámetros de entrada
    numero_unidad = request.GET.get('numero_unidad', '').strip()
    socio = request.GET.get('socio', '').strip().lower()
    placa = request.GET.get('placa', '').strip()
    responsable = request.GET.get('responsable', '').strip()
    contacto = request.GET.get('contacto', '').strip()
    tarifa = request.GET.get('tarifa', '').strip()
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
    if tarifa:
        filters['id_tarifa__nombre_tarifa__icontains'] = tarifa
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
    headers = ['Número Unidad', 'Socio', 'Placa', 'Responsable', 'Contacto', 
               'Tarifa', 'Estado', 'Vencimiento SOAT', 'Vencimiento CIVM']
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
            unidad.id_tarifa.nombre_tarifa if unidad.id_tarifa else "",
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




@login_required       
def listar_control_unidades(request):
    numero_control = request.GET.get('numero_control', '').strip()
    numero_unidad = request.GET.get('numero_unidad', '').strip()
    vuelta = request.GET.get('vuelta', '').strip()
    date_filterp = request.GET.get('date_filterp', '').strip()
    usuario = request.GET.get('usuario','').strip()

    if numero_control:
        controles = controlUnidades.objects.filter(numero_control__icontains=numero_control)
    elif numero_unidad:
        controles = controlUnidades.objects.filter(unidad__numero_unidad__icontains=numero_unidad)
    elif vuelta:
        controles = controlUnidades.objects.filter(vuelta__icontains=vuelta)
    elif date_filterp:
        try:
            month, year = map(int, date_filterp.split('/'))
            controles = controles.filter(fecha_vuelta__month=month, fecha_vuelta__year=year)
        except ValueError:
            pass
    elif usuario:
        controles = controlUnidades.objects.filter(usuario__icontains = usuario)
    else: 
        controles = controlUnidades.objects.all()
        
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
        'date_filterp': date_filterp,
        'usuario': usuario
    })

@login_required       
def listar_tarifas(request):
    tarifas = tarifa.objects.all()
    for tarif in tarifas:
        tarif.nombre_tarifa_display = tarif.nombre_tarifa  
        tarif.monto_display = f"S/ {float(tarif.monto):,.2f}"
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
    numero_pago = request.GET.get('numero_pago', '').strip()
    vuelta = request.GET.get('vuelta', '').strip()
    numero_unidad = request.GET.get('numero_unidad', '').strip()
    nombre_tarifa = request.GET.get('nombre_tarifa', '').strip()
    metodo_pago = request.GET.get('metodo_pago', '').strip()
    date_filterp = request.GET.get('date_filterp', '').strip()
    detalle = request.GET.get('detalle', '').strip()
    usuario = request.GET.get('usuario', '').strip()

    pagos_list = pagos.objects.all()

    if numero_pago:
        pagos_list = pagos_list.filter(id_pago__icontains=numero_pago)
    elif vuelta:
        pagos_list = pagos_list.filter(id_control__vuelta__icontains=vuelta)
    elif numero_unidad:
        pagos_list = pagos_list.filter(id_control__unidad__numero_unidad__icontains=numero_unidad)
    elif nombre_tarifa:
        pagos_list = pagos_list.filter(id_control__unidad__id_tarifa__nombre_tarifa__icontains=nombre_tarifa)
    elif metodo_pago:
        pagos_list = pagos_list.filter(id_metodo__tipo__icontains=metodo_pago)
    elif date_filterp:
        try:
            month, year = map(int, date_filterp.split('/'))
            pagos_list = pagos_list.filter(fecha_pago__month=month, fecha_pago__year=year)
        except ValueError:
            pass
    elif detalle:
        pagos_list = pagos_list.filter(detalle__icontains=detalle)
    elif usuario:
        pagos_list = pagos_list.filter(usuario__username__icontains=usuario)  # Filtra por nombre de usuario

    for pago in pagos_list:
        pago.vuelta_display = pago.id_control.vuelta if pago.id_control else "N/A"
        pago.numero_unidad_display = pago.id_control.unidad.numero_unidad if pago.id_control and pago.id_control.unidad else "N/A"
        pago.nombre_tarifa_display = pago.id_control.unidad.id_tarifa.nombre_tarifa if pago.id_control and pago.id_control.unidad and pago.id_control.unidad.id_tarifa else "N/A"
        pago.metodo_pago_display = pago.id_metodo.tipo if pago.id_metodo else "N/A"
        pago.fecha_pago_display = pago.fecha_pago.strftime('%d/%m/%Y') if pago.fecha_pago else "N/A"
        pago.detalle_display = pago.detalle
        pago.usuario_display = pago.usuario.username if pago.usuario else "N/A"  # Muestra el nombre de usuario

    return render(request, 'pagos/listar_pagos.html', {
        'pagos_list': pagos_list,
        'numero_pago': numero_pago,
        'vuelta': vuelta,
        'numero_unidad': numero_unidad,
        'nombre_tarifa': nombre_tarifa,
        'metodo_pago': metodo_pago,
        'date_filterp': date_filterp,
        'detalle': detalle,
        'usuario': usuario
    })



@login_required
def crear_control_unidad(request):
    if request.method == 'POST':
        form = ControlUnidadesForm(request.POST, user=request.user)
        if form.is_valid():
            control_unidad = form.save(commit=False)
            control_unidad.save()
            return redirect('listar_control_unidades')
    else:
        initial_data = {}
        if 'unidad' in request.GET:
            unidad_id = request.GET.get('unidad')
            try:
                unidad = UnidadTransporte.objects.get(id=unidad_id)
                ultimo_control = controlUnidades.objects.filter(unidad=unidad).order_by('-vuelta').first()
                initial_data['vuelta'] = (ultimo_control.vuelta + 1) if ultimo_control else 1
            except UnidadTransporte.DoesNotExist:
                pass
        
        form = ControlUnidadesForm(initial=initial_data, user=request.user)
    
    return render(request, 'control_unidades/crear_control.html', {'form': form})

@login_required
def crear_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)  # Crea el objeto pero no lo guarda todavía
            pago.usuario = request.user     # Asigna el usuario actual
            pago.save()                     # Guarda el objeto con el usuario asignado
            return redirect('listar_pagos')  # Redirige a la lista de pagos o donde prefieras
    else:
        form = PagoForm()
    return render(request, 'pagos/crear_pagos.html', {'form': form})

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