from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='index'),
    path('carga/', views.carga,name='carga'),
    path('datos/', views.datos ,name='datos'),
    path('reset/', views.reset ,name='reset'),
    #path('resumenIva/', views.resumenIva ,name='resumenIva'),
    #path('resumenFechas/', views.resumenFechas ,name='resumenFechas'),
    path('info/', views.info ,name='info'),
    path('ayuda/', views.ayuda ,name='ayuda'),
]