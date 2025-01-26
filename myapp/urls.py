from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('transporte/', views.transporte, name="transporte"),
    path('hello/<str:username>', views.hello, name="hello"),
    path('logout/', views.exit, name='exit'),
    path('listar_unidades/', views.listar_unidades, name='listar_unidades'),
    path('crear_unidad/', views.crear_unidad, name='crear_unidad'),
    path('control_unidades/', views.listar_control_unidades, name='listar_control_unidades'),
    path('tarifas/', views.listar_tarifas, name='listar_tarifas'),
    path('metodos/', views.lista_metodos_pago, name= 'lista_metodos_pago'),
    path('listar_pagos/', views.listar_pagos, name='listar_pagos'),
    path('CrearControl/', views.crear_control_unidad, name='crear_control_unidad'),
    path('CrearPagos/', views.crear_pago, name='crear_pago'),
    path('licencias/', views.listar_licencias, name='listar_licencias'),
    path('crear_licencias/', views.crear_licencias, name='crear_licencias'),
    path('editar_licencia/<int:id>/', views.editar_licencia, name='editar_licencia'),
    path('unidades/exportar/', views.exportar_unidades_excel, name='exportar_unidades_excel'),
    path('licencias/exportar/', views.exportar_licencias_excel, name='exportar_licencias_excel'),
    path('unidades/editar/<int:id_transporte>/', views.editar_unidad, name='editar_unidad'),
    path('control_unidades/editar/<int:id_control>/', views.editar_control_unidad, name='editar_control_unidad'),
    path('api/get_vuelta/<int:unidad_id>/', views.obtener_vuelta_actual, name='get_vuelta_actual'),
]
