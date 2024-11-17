from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('hello/<str:username>', views.hello, name="hello"),
    path('projects/', views.projects, name="project"),  
    path('logout/', views.exit, name='exit'),
    path('listar_unidades/', views.listar_unidades, name='listar_unidades'),
    path('crear_unidad/', views.crear_unidad, name='crear_unidad'),
    path('listar_stock/', views.listar_stock, name='listar_stock'),
    path('crear_stock/', views.crear_stock, name='crear_stock'),
    path('crear_contadores_surtidor/', views.crear_contadores_surtidor, name='crear_contadores_surtidor'),
    path('control_unidades/', views.listar_control_unidades, name='listar_control_unidades'),
    path('tarifas/', views.listar_tarifas, name='listar_tarifas'),
    path('metodos/', views.lista_metodos_pago, name= 'lista_metodos_pago'),
    path('listar_pagos/', views.listar_pagos, name='listar_pagos'),
    path('CrearControl/', views.crear_control_unidad, name='crear_control_unidad'),
    path('CrearPagos/', views.crear_pago, name='crear_pago'),

]
