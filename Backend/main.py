from manager import Manager
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask.json import jsonify
from xml.etree import ElementTree as ET
from flask_cors import CORS

app = Flask(__name__)

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


@app.route('/add', methods=['POST'])
def add():
    xml = request.get_data().decode('utf-8')
    raiz = ET.XML(xml)
    for elemento in raiz:
        nombre = ''
        tipo = ''
        edad = 0
        for subelemnto in elemento:
            if subelemnto.tag == 'nombre':
                nombre = subelemnto.text
            if subelemnto.tag == 'tipo':
                tipo = subelemnto.text
            if subelemnto.tag == 'edad':
                edad = subelemnto.text
        manage.agregar_mascota(nombre, tipo, edad)
    return jsonify({'ok' : True, 'msg':'Macota insertada a la BD con exito'}), 200

@app.route('/getmascotas')
def get_pets():
    return jsonify(manage.obtener_mascotas()), 200


if __name__=='__main__':
    app.run(debug=True, port=4000)