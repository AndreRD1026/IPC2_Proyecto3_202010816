from alias import Alias

class Servicio():
    def __init__(self, nombre):
        self.nombre = nombre
        self.alias = []

    def agregar_alias(self, alias):
        al = Alias(alias)
        self.alias.append(al)

    def obtener_alias(self):
        json = []
        for ali in self.alias:
            ali = {
                'alias' : ali.alias
            }
            json.append(ali)
        return json