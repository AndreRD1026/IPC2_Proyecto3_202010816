class palabras_b():
    def __init__(self,tipo, palabra):
        self.tipo = tipo 
        self.palabra = palabra
    def __repr__(self):
        return f'\n Tipo: {self.tipo} Palabra: {self.palabra}'

class Nose():
    def __init__(self,empresa, servicio):
        self.servicio = servicio
        self.empresa = empresa 
        
    def __repr__(self):
        return f'\n Servicio: {self.servicio} Empresa: {self.empresa}'

class vicio():
    def __init__(self,servicio, alias):
        self.servicio = servicio
        self.alias = alias 
        
    def __repr__(self):
        return f'\n Servicio: {self.servicio} Alias: {self.alias}'

class fech():
    def __init__(self,fecha,total,t_positivo,t_negativo,t_neutro):
        self.fecha =fecha
        self.total = total
        self.t_positivo = t_positivo
        self.t_negativo = t_negativo
        self.t_neutro = t_neutro

    def __repr__(self):
        return f'\n Fecha: {self.fecha} Total: {self.total} Positivo: {self.t_positivo} Negativo: {self.t_negativo} Neutro: {self.t_neutro}'

class men_empr():
    def __init__(self,fecha,empresa,total,t_positivo,t_negativo,t_neutro):
        self.fecha=fecha
        self.empresa =empresa
        self.total = total
        self.t_positivo = t_positivo
        self.t_negativo = t_negativo
        self.t_neutro = t_neutro

    def __repr__(self):
        return f'\n Fecha: {self.fecha} Empresa: {self.empresa} Total: {self.total} Positivo: {self.t_positivo} Negativo: {self.t_negativo} Neutro: {self.t_neutro}'

class men_servi():
    def __init__(self,fecha,empre,servicio,total,t_positivo,t_negativo,t_neutro):
        self.fecha = fecha
        self.empre=empre
        self.servicio =servicio
        self.total = total
        self.t_positivo = t_positivo
        self.t_negativo = t_negativo
        self.t_neutro = t_neutro

    def __repr__(self):
        return f'\n Fecha: {self.fecha} Empresa: {self.empre} Servicio: {self.servicio} Total: {self.total} Positivo: {self.t_positivo} Negativo: {self.t_negativo} Neutro: {self.t_neutro}'
class Men():
    def __init__(self,fecha, empresa, servicio, estado):
        self.fecha = fecha 
        self.empresa =empresa
        self.servicio =servicio
        self.estado = estado 
    def __repr__(self):
        return f'\n Fecha: {self.fecha} Empresa: {self.empresa} Servicio: {self.servicio} Estado: {self.estado}'