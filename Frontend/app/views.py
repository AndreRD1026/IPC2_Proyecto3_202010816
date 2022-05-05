import os
import webbrowser
from django.shortcuts import render
from matplotlib.style import context
from numpy import character
import requests
from requests.sessions import Request
from app.forms import FileForm
# Create your views here.


endpoint = 'http://127.0.0.1:5000/'


# def home(request):
#     context = {
#         'characters' : []
#     }
#     try:
#         respone = requests.get(endpoint + 'getpalabrasp')
#         characters = respone.json()
#         context['caracteres'] = characters
        
#     except:
#         print("API no está levantada")
#    return render(request, 'index.html', context)


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

# def carga(request):
#     contexto = {
#         'tab' : 'Carga',
#         'contenido': None,
#         'response' : None
#     }

#     if request.method == 'POST':
#         form = FileForm(request.POST, request.FILES)
#         if form.is_valid():
            
#             f = request.FILES['file'].read()
#             response = requests.post(endpoint+"addarchivo",data = f)
#             fo = open("../Backend/salida.xml","r",  encoding='utf8')
#             texto = fo.read()
#             print(texto)

            
#             if response.json()['ok'] == True :
#                 print("Hola")
#                 contexto['contenido']= f.decode('utf-8')
#                 contexto['response']= texto
#             else:
                
#                 contexto['contenido']= f.decode('utf-8')
#                 contexto['response']= 'Error en el archivo XML que se subió'
            
#             fo.close()

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
            response = requests.post(endpoint + 'addVarious', data=xml_binary)
            if response.ok:
                ctx['response'] = 'Archivo XML cargado corrrectamente'
            else:
                ctx['response'] = 'El archivo se envio, pero hubo un error en el servidor'
    else:
        return render(request, 'carga.html')
    return render(request, 'carga.html', ctx)


def mensaje(request):
    ctx = {
        'tab' : 'Mensaje',
        'content':None,
        'response':None
    }
    if request.method == 'POST' and 'Enviar' in request.POST:
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            xml_binary = f.read()
            xml = xml_binary.decode('utf-8')
            ctx['xml'] = xml
            response = requests.post(endpoint + 'add', data=xml_binary)
            if response.ok:
                ctx['response'] = 'Archivo XML cargado corrrectamente'
            else:
                ctx['response'] = 'El archivo se envio, pero hubo un error en el servidor'
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

def ayuda(request):
    contexto={
        'tab' : 'Inicio'
    }
    print('file:///' + os.getcwd())
    webbrowser.open('file:///' + os.getcwd()+ '/app/static/ensayo.pdf')
    return render(request,'index.html',contexto)
