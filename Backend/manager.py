from datetime import datetime
from operator import neg
import re
from turtle import st
from positivos import positivos
from negativos import negativos
from empresa import Empresa
from mensajes import mensajes

class Manager():
    def __init__(self):
        self.positivos = []
        self.negativos = []
        self.empresas = []
        self.mensajes = []


    def agregar_palabra_pos(self, palabra):
        palabra_pos = positivos(palabra)
        self.positivos.append(palabra_pos)

    def agregar_palabra_neg(self, palabra):
        palabra_neg = negativos(palabra)
        self.negativos.append(palabra_neg)

    def agregar_empresa(self, nombre):
        empr = Empresa(nombre)
        self.empresas.append(empr)

    def agregar_mensajes(self, lugar, fecha, hora,usuario, red,mensaje):
        nuevo_men = mensajes(lugar, fecha, hora, usuario, red, mensaje)
        self.mensajes.append(nuevo_men)

    def obtener_palabras_pos(self):
        json = []
        for positivo in self.positivos:
            positivo = {
                'palabra_pos' : positivo.palabra
            }
            json.append(positivo)
        return json

    def obtener_palabras_neg(self):
        json = []
        for negativo in self.negativos:
            negativo = {
                'palabra_neg' : negativo.palabra
            }
            json.append(negativo)
        return json

    def obtener_empresa(self):
        json = []
        for empresa in  self.empresas:
            empresa = {
                'nombre' : empresa.nombre,
                'servicios' : empresa.obtener_servicio()
            }
            json.append(empresa)
        return json

    def obtener_mensajes(self):
        json = []
        for mensaje in self.mensajes:
            mensaje = {
                'Lugar' : mensaje.lugar,
                'fecha' : mensaje.fecha,
                'hora' : mensaje.hora,
                'usuario' : mensaje.usuario,
                'red' : mensaje.red,
                'mensaje' : mensaje.mensaje      
            }
            json.append(mensaje)
        return json

    def comprobarFecha(self):
        dia = int(self.fecha.split("/")[0])
        mes = int(self.fecha.split("/")[1])
        anio = int(self.fecha.split("/")[2])
        try:
            fecha = datetime.datetime(anio,mes,dia)
            self.fechaCorrecta = True
        except:
            self.fechaCorrecta = False

    def analizararchivo(self):
        global countP
        patron = re.compile(r'\S+')
        countP = 0
        countN = 0
        countNe = 0
        empresamencionada = []
        serviciomencionado = []
        strJson = '['
        for mensaje in self.mensajes:
            positivos = 0
            negativos = 0
            palabras = patron.findall(mensaje.mensaje)
            for palabra in palabras:
                for positivo in self.positivos:
                    if palabra == str(positivo.palabra).strip():
                        positivos += 1
                for negativo in self.negativos:
                    if palabra == str(negativo.palabra).strip():
                        negativos += 1
                for empresa in self.empresas:
                    if palabra == str(empresa.nombre).strip():
                        empresamencionada.append(empresa.nombre.replace('\n','').replace('\t',''))
                    for servicio in empresa.servicios:
                        if palabra == str(servicio.nombre).strip() and servicio.nombre not in serviciomencionado:
                            serviciomencionado.append(servicio.nombre.replace('\n','').replace('\t',''))
                        for alias in servicio.alias:
                            if palabra == str(alias.alias).strip() and servicio.nombre not in serviciomencionado:
                                serviciomencionado.append(servicio.nombre.replace('\n','').replace('\t',''))

            if positivos > negativos:
                countP += 1
                strJson += '["{}","{}",{},{},"{}"]\n,'.format(mensaje.mensaje.replace('\n','').replace('\t',''), 'Mensaje :Positivo', empresamencionada, serviciomencionado, mensaje.fecha)
                
            elif positivos < negativos:
                countN += 1
                #print("Cantidad negativos: " + str(countN))
                strJson += '["{}","{}",{},{},"{}"]\n,'.format(mensaje.mensaje.replace('\n','').replace('\t',''), 'Mensaje: Negativo', empresamencionada, serviciomencionado, mensaje.fecha)
            elif positivos == negativos:
                countNe += 1
                #print("Cantidad neutros: " + str(countNe))
                strJson += '["{}","{}",{},{},"{}"]\n,'.format(mensaje.mensaje.replace('\n','').replace('\t',''), 'Mensaje: Neutro', empresamencionada, serviciomencionado, mensaje.fecha)
            
        if strJson != '[':
            strJson = strJson[:-1] + ']'
            Json = eval(strJson)
            print(str(Json))

            
        
        

    def crearArchivoAlmacenamiento(self):
        pass

    def resumenporFecha(self, fecha, empresa, empresas):
        pass

    def resumenporRangoFecha(self, fecha1, fecha2, empresa, empresas):
        pass