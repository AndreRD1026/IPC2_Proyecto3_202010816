import os
import webbrowser
from django.shortcuts import render
from matplotlib.style import context
from numpy import character
import requests
from requests.sessions import Request
from app.forms import RangoForm
from app.forms import FileForm
from app.forms import MensajeForm
# Create your views here.


endpoint = 'http://127.0.0.1:5000/'

def home(request):
    contexto={
        'tab' : 'Inicio'
    }
    response = requests.get(endpoint)
    respuesta = response.json()
    return render(request,'index.html',contexto)

def reset(request):
    contexto = {
        'tab' : 'Consulta de Datos',
        
    }
    if request.method == 'POST':        
            
            response = requests.delete(endpoint+"reset")
            contexto['contenido']= ''
            contexto['response']= 'Se eliminaron los datos'
                
            
    return render(request,'datos.html',contexto)

def carga(request):
    ctx = {
        'tab' : 'Carga',
        'content':None,
        'response':None
    }
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            xml_binary = f.read()
            xml = xml_binary.decode('utf-8')
            ctx['content'] = xml
            response = requests.post(endpoint + 'crearsalida', data=xml_binary)
            if response.ok:
                #ctx['response'] = 'Archivo xml cargado exitosamente'
                response = requests.get(endpoint + 'getsalida')
                datos = response.text
                ctx['response'] = datos
            else:
                ctx['response'] = 'El archivo se envio, pero hubo un error en el servidor'
    else:
        return render(request, 'carga.html')
    return render(request, 'carga.html', ctx)

def resumenMensaje(request):
    
    contexto={
        'tab' : 'Consulta de Datos',
        'Fecha': None,
        'Respuesta': None
    }

    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            jsonDatos = form.cleaned_data
            print(jsonDatos)
            if len(str(jsonDatos['fecha'].month)) == 1:
                mes = "0"+str(jsonDatos['fecha'].month)
            else:
                mes = str(jsonDatos['fecha'].month)
            
            if len(str(jsonDatos['fecha'].day)) == 1:
                dia = "0"+str(jsonDatos['fecha'].day)
            else:
                dia = str(jsonDatos['fecha'].day)

            fecha = dia + "-"+ mes +"-"+str(jsonDatos['fecha'].year)
            print(fecha)
            response = requests.get(endpoint + "resumenMensaje/" + fecha )
            print(response.json())
            contexto['Fecha'] = fecha
            contexto['Respuesta'] = response.json()
            print(contexto['Respuesta'])
            print(contexto)
            
    return render(request,'resumenMensaje.html',contexto)

def resumenFechas(request):
    contexto={
        'tab' : 'Consulta de Datos',
        'Fecha1': None,
        'Fecha2':None,
        'Respuesta': None
    }
    if request.method == 'POST':
        form = RangoForm(request.POST)
        if form.is_valid():
            jsonDatos = form.cleaned_data
            print(jsonDatos)
            if len(str(jsonDatos['fecha1'].month)) == 1:
                mes1 = "0"+str(jsonDatos['fecha1'].month)
            else:
                mes1 = str(jsonDatos['fecha1'].month)
            
            if len(str(jsonDatos['fecha1'].day)) == 1:
                dia1 = "0"+str(jsonDatos['fecha1'].day)
            else:
                dia1 = str(jsonDatos['fecha1'].day)

            fecha1 = dia1 + "-"+ mes1 +"-"+str(jsonDatos['fecha1'].year)

            if len(str(jsonDatos['fecha2'].month)) == 1:
                mes2 = "0"+str(jsonDatos['fecha2'].month)
            else:
                mes2 = str(jsonDatos['fecha2'].month)
            
            if len(str(jsonDatos['fecha2'].day)) == 1:
                dia2 = "0"+str(jsonDatos['fecha2'].day)
            else:
                dia2 = str(jsonDatos['fecha2'].day)

            fecha2 = dia2 + "-"+ mes2 +"-"+str(jsonDatos['fecha2'].year)
            valor = jsonDatos['valor']
            response = requests.get(endpoint + "resumenRangoFechas/" + fecha1+"/"+fecha2 + "/" + valor)
            print(response.json())
            contexto['Fecha1'] = fecha1
            contexto['Fecha2'] = fecha2
            contexto['Respuesta'] = response.json()
        

    
    return render(request,'resumenFechas.html',contexto)
def info(request):
    contexto={
        'tab' : 'Ayuda'
    }
    return render(request,'info.html',contexto)


def mensaje(request):
    ctx = {
        'tab' : 'Mensaje',
        'content':None,
        'response':None
    }
    if request.method == 'POST' and 'Enviar Mensaje' in request.POST:
        form = FileForm(request.POST)
        if form.is_valid():
            #f = request.FILES['file']
            #xml_binary = f.read()
            cadena = request
            ctx['content'] = cadena
            response = requests.post(endpoint + 'mandarmensaje')
            if response.ok:
                
                ctx['answer'] = 'Mensaje leido'
            else:
                ctx['answer'] = 'El archivo se envio, pero hubo un error en el servidor'
    elif request.method == 'POST' and 'Resetear Base de Datos' in request.POST:
        ctx = {
            'message' : None,
            'answer' : None
        }
    else:
        return render(request, 'mensaje.html')
    return render(request, 'mensaje.html', ctx)


def datos(request):
    return render(request, 'datos.html')

def info(request):
    contexto={
        'tab' : 'Ayuda'
    }
    return render(request,'info.html',contexto)


def reset(request):
    contexto = {
        'tab' : 'Carga',
        
    }
    if request.method == 'POST':        
            
            response = requests.delete(endpoint + 'reset')
            contexto['contenido']= ''
            contexto['response']= 'Se eliminaron los datos'
                
    return render(request,'carga.html',contexto)

def ayuda(request):
    contexto={
        'tab' : 'Inicio'
    }
    print('file:///' + os.getcwd())
    webbrowser.open('file:///' + os.getcwd()+ '/app/static/ensayo.pdf')
    return render(request,'index.html',contexto)
