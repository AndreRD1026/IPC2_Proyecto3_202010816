from operator import neg
from mascota import Mascota
from positivos import positivos
from negativos import negativos
from empresa import Empresa

class Manager():
    def __init__(self):
        self.mascotas = []
        self.positivos = []
        self.negativos = []
        self.empresas = []


    def agregar_mascota(self, n, a, e):
        nuevo = Mascota(n, a, e)
        self.mascotas.append(nuevo)

    def agregar_palabra_pos(self, palabra):
        palabra_pos = positivos(palabra)
        self.positivos.append(palabra_pos)

    def agregar_palabra_neg(self, palabra):
        palabra_neg = negativos(palabra)
        self.negativos.append(palabra_neg)

    def agregar_empresa(self, nombre,servicios,alias):
        empresa = Empresa(nombre,servicios,alias)
        self.empresas.append(empresa)

    
    def obtener_mascotas(self):
        json = []
        for mascota in self.mascotas:
            mascota = {
                'nombre' : mascota.nombre,
                'tipo' : mascota.animal,
                'edad' : mascota.edad
            }
            json.append(mascota)
        return json

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

    def obtener_empresas(self):
        json = []
        for empresa in self.empresas:
            empresa = {
                'Nombre' : empresa.nombre,
                'Servicio' : empresa.servicios,
                'Alias' : empresa.alias
            }
            json.append(empresa)
        return json

    def crearArchivoAlmacenamiento(self):
        pass

    def resumenporFecha(self, fecha, empresa, empresas):
        pass

    def resumenporRangoFecha(self, fecha1, fecha2, empresa, empresas):
        pass