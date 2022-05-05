from turtle import position
import unicodedata
from unittest import result
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
listasalida = []
listapalabras = []
listapalabrasn = []
listamensajes = []
new_palabras = []
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
    global mensaje
    global fecha
    global palabra_p
    global palabra_neg
    global new_palabras
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
                            listapalabras = normalize(subelemento1.text.strip())
                            print("Palabra: " + listapalabras)
                            #manage.agregar_palabra_pos(subelemento1.text.strip())
                            manage.agregar_palabra_pos(listapalabras)
                if subelemento.tag == 'sentimientos_negativos':
                    for subelemento1 in subelemento:
                        if subelemento1.tag == 'palabra':
                            listapalabrasn = normalize(subelemento1.text)
                            print("Neg:" + listapalabrasn)
                            #manage.agregar_palabra_neg(subelemento1.text.strip())
                            manage.agregar_palabra_neg(listapalabrasn)

                if subelemento.tag == 'empresas_analizar':
                    index = 0
                    for subelemento1 in subelemento:
                        for subelemento2 in subelemento1:
                            if subelemento2.tag == 'nombre':

                                manage.agregar_empresa(subelemento2.text)
                                index2 = 0
                            if subelemento2.tag == 'servicio':
                                nuevoservicio = normalize(subelemento2.attrib['nombre'])
                                manage.empresas[index].agregar_servicio(nuevoservicio)
                                
                                for subelemento3 in subelemento2:
                                    nuevoalias = normalize(subelemento3.text)
                                    manage.empresas[index].servicios[index2].agregar_alias(nuevoalias)
                                index2 += 1
                        index += 1
        #####Mensajes
        if elemento.tag == 'lista_mensajes':
            for subelemento in elemento:
                if subelemento.tag == 'mensaje':
                    expresion_re = re.compile(r'(\D+:)\s+(\D+),\s+(\d+\D\d+\D\d+)\s+(\d+:\d+)\s+(\D+:)\s+(\S+|([^@]+@[^.]+.\S+))\s*(\D+:)\s+(\S+)\s+(\D+)')
                    datosmen = expresion_re.findall(subelemento.text)
                    fecha = (datosmen[0][2])
                    mensaje = normalize(datosmen[0][9])
                    dia = fecha.split("/")[0]
                    mes = fecha.split("/")[1]
                    anio = fecha.split("/")[2]
                    #print("Anio ", anio)
                    mensaje2 = mensaje
                    manage.agregar_mensajes(datosmen[0][1],datosmen[0][2],datosmen[0][3],datosmen[0][5],datosmen[0][8],mensaje2)     
                    #print(fecha)
                    print(mensaje)
                    
                    for i in range (0,len(listadiccionario)):
                        if listadiccionario[i].fecha == fecha:
                            encontrado = True
                            posicion = i
                            print("Dte correcto")
                    #inicioCorrelativo = int(anio+mes+dia)
            

                    
                    
    #analizar()    
    manage.analizararchivo()      
    actualizarXml()   
    return jsonify({'ok' : True, 'msg':'Archivo XML leído correctamente'}), 200


def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


def actualizarXml():
    global listadiccionario
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += "<lista_respuestas>\n"
    for salida in listadiccionario:
        xml += "    <respuesta>\n"
        xml += "        <fecha>" + salida.fecha + "</fecha>\n"
        xml += "        <mensajes>\n"
        xml += "            <total>" + "Total mensajes" + "</total>\n"
        xml += "            <positivos>" + "Cantidad positivos" + "</positivos>\n"
        xml += "            <negativos>" + "Cantidad negativos" + "</negativos>\n"
        xml += "            <neutros>" + "Cantidad neutros" + "</neutros>\n"
        xml += "        </mensajes>\n"
        xml += "       <analisis>\n"
        xml += "        <empresa nombre=>\n"
        xml += "        <mensajes>\n"
        xml += "            <total>" + "Total mensajes" + "</total>\n"
        xml += "            <positivos>" + "Cantidad positivos" + "</positivos>\n"
        xml += "            <negativos>" + "Cantidad negativos" + "</negativos>\n"
        xml += "            <neutros>" + "Cantidad neutros" + "</neutros>\n"
        xml += "        </mensajes>\n"
        xml += "        <servicios>\n"
        xml += "            <servicio nombre=inscripción>\n"
        xml += "        <mensajes>\n"
        xml += "            <total>" + "Total mensajes" + "</total>\n"
        xml += "            <positivos>" + "Cantidad positivos" + "</positivos>\n"
        xml += "            <negativos>" + "Cantidad negativos" + "</negativos>\n"
        xml += "            <neutros>" + "Cantidad neutros" + "</neutros>\n"
        xml += "        </mensajes>\n"
        xml += "            </servicio>\n"
        xml += "        </servicios>\n"
        xml += "        </empresa>\n"
        xml += "       </analisis>\n"
        xml += "     </respuesta>\n"
    xml += "</lista_respuestas>\n"
        
    fo = open("salida.xml","w",  encoding='utf8')
    fo.write(xml)
    fo.close()

@app.route('/getpalabrasp', methods=['GET'])
def get_palabras_poa():
    return jsonify(manage.obtener_palabras_pos()), 200  

@app.route('/getpalabrasn', methods=['GET'])
def get_palabras_neg():
    return jsonify(manage.obtener_palabras_neg()), 200

@app.route('/getempresa', methods=['GET'])
def get_empresas():
    return jsonify(manage.obtener_empresa()), 200


@app.route('/getmensaje', methods=['GET'])
def get_mensaje():
    return jsonify(manage.obtener_mensajes()), 200


@app.route('/getsalida', methods=['GET'])
def get_salida():
    return jsonify(manage.analizararchivo()), 200


@app.route('/reset', methods=['DELETE'])
def reset():
    global listapalabrasn, listapalabras
    listapalabras = []
    listapalabrasn = []
    fo = open("salida.xml","w")
    fo.write("")
    fo.close()
    respuesta = {
        'mensaje' : 'Base reseteada'
    }
    return jsonify(respuesta)
        

if __name__=='__main__':
    app.run(debug=True, port=4000)