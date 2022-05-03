from manager import Manager
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask.json import jsonify
from xml.etree import ElementTree as ET
from flask_cors import CORS

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
@app.route('/agregarDtes', methods=['POST'])
def agregarDTE():
    global listadiccionario
    salida = []
    xmlBien = True
    try:
        xml = request.data.decode('utf-8')
        root = ET.XML(xml)
    except:
        xmlBien = False
    if xmlBien is False:
        mensaje = {
            'ok':False,
            'salida':None
        }
        print("Hola")
        
        return(jsonify(mensaje))
    else:
        numerosBien = True
        for dic in root:
            numerosBien = True
            palabra = dic.find('palabra')
            #referencia = dic.find('REFERENCIA').text.replace("\r","").replace(" ","").replace("\n","")
            #nitE = dic.find('NIT_EMISOR').text.replace("\r","").replace(" ","").replace("\n","")
            #nitR = dic.find('NIT_RECEPTOR').text.replace("\r","").replace(" ","").replace("\n","")
            # try:
            #     valor = float(dte.find('VALOR').text.replace("\r",""))
            #     iva = float(dte.find('IVA').text.replace("\r",""))
            #     total = float(dte.find('TOTAL').text.replace("\r",""))
            # except:
            numerosBien = False
            if numerosBien is False:
                objeto={
                        'Mensaje': 'DTE Correcto'
                    }
                salida.append(objeto)
            else:
                objeto={
                        'Mensaje' : 'ERROR'
                }
                salida.append(objeto)

@app.route('/addarchivo', methods=['POST'])
def addarchivo():
    palabra_pos = ''
    palabra_neg = ''
    subelemento1 = ''
    xml = request.get_data().decode('utf-8')
    raiz = ET.XML(xml)
    for elemento in raiz:
        for subelemento in elemento:
            if subelemento.tag == 'sentimientos_positivos':
                for subelemento1 in subelemento:
                    if subelemento1.tag == 'palabra':
                        #palabra_pos = subelemento1.text.strip()
                        manage.agregar_palabra_pos(subelemento1.text.strip())
            if subelemento.tag == 'sentimientos_negativos':
                for subelemento1 in subelemento:
                    if subelemento1.tag == 'palabra':
                        #palabra_neg = subelemento1.text.strip()
                        manage.agregar_palabra_neg(subelemento1.text.strip())
            # if subelemento.tag == 'empresas_analizar':
            #     for subelemento1 in subelemento:
            #         for subelemento2 in subelemento1:
            #             if subelemento2.tag == 'nombre':
            #                 nombre = subelemento2.text
            #             if subelemento2.tag == 'servicio':
            #                 servicio = subelemento2.attrib
            #             if subelemento2.tag == 'alias':
            #                 alias = subelemento2.text
        #manage.agregar_palabra_pos(palabra_pos)
        #manage.agregar_palabra_neg(palabra_neg)
        #manage.agregar_empresa(nombre,servicio,alias)
    return jsonify({'ok' : True, 'msg':'Palabras insertada a la BD con exito'}), 200

@app.route('/getpalabrasp')
def get_palabras_poa():
    return jsonify(manage.obtener_palabras_pos()), 200  

@app.route('/getpalabrasn')
def get_palabras_neg():
    return jsonify(manage.obtener_palabras_neg()), 200

@app.route('/getempresas')
def get_empresas():
    return jsonify(manage.agregar_empresa()), 200
        

if __name__=='__main__':
    app.run(debug=True, port=4000)