from operator import neg
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

    def crearArchivoAlmacenamiento(self):
        pass

    def resumenporFecha(self, fecha, empresa, empresas):
        pass

    def resumenporRangoFecha(self, fecha1, fecha2, empresa, empresas):
        pass