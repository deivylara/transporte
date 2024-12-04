from django.urls import path
from . import views

urlpatterns = [
    path('', views.grifo, name="grifo"),
    path('listar_stock/', views.listar_stock, name='listar_stock'),
    path('crear_stock/', views.crear_stock, name='crear_stock'),
    path('crear_contadores_surtidor/', views.crear_contadores_surtidor, name='crear_contadores_surtidor'),
]