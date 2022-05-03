from manager import Manager
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask.json import jsonify
from xml.etree import ElementTree as ET
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)
listadiccionario = []
manage = Manager()

#@app.route('/')
#def index():
#    return 'Hola, soy una API', 200

@app.route('/', methods=['GET'])
def prueba():
    objeto={
        'Mensaje': 'INICIO'
    }
    return(jsonify(objeto))

#Métodos POST
@app.route('/addarchivo', methods=['POST'])
def addarchivo():
    palabra_pos = ''
    palabra_neg = ''
    subelemento1 = ''
    xml = request.get_data().decode('utf-8')
    raiz = ET.XML(xml)
    for elemento in raiz:
        if elemento.tag == 'diccionario':
            for subelemento in elemento:
                if subelemento.tag == 'sentimientos_positivos':
                    for subelemento1 in subelemento:
                        if subelemento1.tag == 'palabra':
                            manage.agregar_palabra_pos(subelemento1.text.strip())
                if subelemento.tag == 'sentimientos_negativos':
                    for subelemento1 in subelemento:
                        if subelemento1.tag == 'palabra':
                            manage.agregar_palabra_neg(subelemento1.text.strip())

                if subelemento.tag == 'empresas_analizar':
                    index = 0
                    for subelemento1 in subelemento:
                        for subelemento2 in subelemento1:
                            if subelemento2.tag == 'nombre':

                                manage.agregar_empresa(subelemento2.text)
                                index2 = 0
                            if subelemento2.tag == 'servicio':
                                manage.empresas[index].agregar_servicio(subelemento2.attrib['nombre'])
                                
                                for subelemento3 in subelemento2:
                                    manage.empresas[index].servicios[index2].agregar_alias(subelemento3.text)
                                index2 += 1
                        index += 1
        #####Mensajes
        if elemento.tag == 'lista_mensajes':
            for subelemento in elemento:
                if subelemento.tag == 'mensaje':
                    expresion_re = re.compile(r'(\D+:)\s+(\D+),\s+(\d+\D\d+\D\d+)\s+(\d+:\d+)\s+(\D+:)\s+(\S+|([^@]+@[^.]+.\S+))\s*(\D+:)\s+(\S+)\s+(\D+)')
                    datosmen = expresion_re.findall(subelemento.text)
                    manage.agregar_mensajes(datosmen[0][1],datosmen[0][2],datosmen[0][3],datosmen[0][5],datosmen[0][8],datosmen[0][9])
                    # info = subelemento.text.replace("\r","").replace("\n","").replace('\t',"")
                    # #print(info)
                    # lugarfecha = info.split(',')
                    # lugar = lugarfecha[0]
                    # fecha = lugarfecha[1].split(" ")[1]
                    # hora = lugarfecha[1].split(" ")[2]
                    # usuario = lugarfecha[1].split(" ")[4]
                    # red = lugarfecha[1].split(" ")[7]
                    # mensaje = lugarfecha[1].split("")[8]
                    # print(lugar)
                    # print("Fecha " , fecha)
                    # print("Hora", hora)
                    # print("Usuario", usuario)
                    # print("Red", red)
                    # print(mensaje)

    return jsonify({'ok' : True, 'msg':'Archivo XML leído correctamente'}), 200

@app.route('/getpalabrasp')
def get_palabras_poa():
    return jsonify(manage.obtener_palabras_pos()), 200  

@app.route('/getpalabrasn')
def get_palabras_neg():
    return jsonify(manage.obtener_palabras_neg()), 200

@app.route('/getempresa')
def get_empresas():
    return jsonify(manage.obtener_empresa()), 200


@app.route('/getmensaje')
def get_mensaje():
    return jsonify(manage.obtener_mensajes()), 200
        

if __name__=='__main__':
    app.run(debug=True, port=4000)