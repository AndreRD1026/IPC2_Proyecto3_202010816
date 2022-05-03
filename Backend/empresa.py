from servicios import Servicio

class Empresa():
    def __init__(self,nombre):
        self.nombre = nombre
        self.servicios = []


    def agregar_servicio(self, nombre):
        serv = Servicio(nombre)
        self.servicios.append(serv)

    def obtener_servicio(self):
        json = []
        for servicio in  self.servicios:
            servicio = {
                'nombre' : servicio.nombre,
                'alias' : servicio.obtener_alias()
            }
            json.append(servicio)
        return json