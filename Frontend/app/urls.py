from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='index'),
    path('cargar/', views.carga,name='carga'),
    path('mensaje/', views.mensaje,name='mensaje'),
    path('datos/', views.datos ,name='datos'),
    path('resumenMensaje/', views.resumenMensaje, name='resumenMensaje'),
    path('resumenFechas/', views.resumenFechas ,name='resumenFechas'),
    path('reset/', views.reset ,name='reset'),
    path('info/', views.info ,name='info'),
    path('ayuda/', views.ayuda ,name='ayuda'),
]