from turtle import position
import unicodedata
from unittest import result
from objetos import Men, fech, men_empr, men_servi, palabras_b, vicio, corto
from manager import Manager
from flask import Flask,Response, jsonify, request
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
mensaje_corto=[]
manage = Manager()

prueba = []
ob_fecha=[]
otro = []
empre = []
ser =[]
ob_men=[]
list_fecha=[]
sinrepe=[]
aux_c_servicios=[]
cantidad_mensaje=[]
cantidad_empresa=[]
cantidad_servicio=[]
nose=[]
apex=[]


#@app.route('/')
#def index():
#    return 'Hola, soy una API', 200

@app.route('/', methods=['GET'])
def prueba1():
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
    LecturaDatos()
    xml = request.get_data().decode('utf-8')
    raiz = ET.XML(xml)
    for elemento in raiz:
        if elemento.tag == 'diccionario':
            for subelemento in elemento:
                if subelemento.tag == 'sentimientos_positivos':
                    for subelemento1 in subelemento:
                        if subelemento1.tag == 'palabra':
                            listapalabras = normalize(subelemento1.text.strip())
                            #print("Palabra: " + listapalabras)
                            #manage.agregar_palabra_pos(subelemento1.text.strip())
                            manage.agregar_palabra_pos(listapalabras)
                if subelemento.tag == 'sentimientos_negativos':
                    for subelemento1 in subelemento:
                        if subelemento1.tag == 'palabra':
                            listapalabrasn = normalize(subelemento1.text)
                            #print("Neg:" + listapalabrasn)
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
                    #print(mensaje)
                    
                    for i in range (0,len(listadiccionario)):
                        if listadiccionario[i].fecha == fecha:
                            encontrado = True
                            posicion = i
                            #print("Dte correcto")
                    #inicioCorrelativo = int(anio+mes+dia)
    manage.analizararchivo()
    return jsonify({'ok' : True, 'msg':'Archivo XML leído correctamente'}), 200


def LecturaDatos():
    try:
        global apex
        global prueba
        global otro
        global empre
        global ser
        global nose
        global ob_men
        global list_fecha
        global sinrepe
        global cantidad_mensaje
        global cantidad_empresa
        global cantidad_servicio
        global aux_c_servicios

        xml = request.get_data().decode('utf-8')
        root = ET.XML(xml)
        for Solicitud in root:

            for diccionario in Solicitud.iter('diccionario'):


                for positivos in diccionario.iter('sentimientos_positivos'):
                    for palabras in positivos.iter('palabra'):
                        po = str(palabras.text).replace(' ','').lower()
                        po = elimina_tildes(po)
                        prueba.append(palabras_b('p',po)) 
                
                for negativos in diccionario.iter('sentimientos_negativos'):
                    for palabras in negativos.iter('palabra'):
                        neg = str(palabras.text).replace(' ','').lower()
                        neg = elimina_tildes(neg)
                        prueba.append(palabras_b('n',neg))
                #print(repr(prueba))

                for analizar in diccionario.iter('empresas_analizar'):
                    for empresa in analizar.iter('empresa'):
                        m = str(empresa[0].text).replace(' ','').lower()
                        m= elimina_tildes(m)
                        empre.append(m)
                        j=1
                        for servicio in empresa.iter('servicio'):
                            servi = str(empresa[j].attrib['nombre']).replace(' ','').lower()
                            servi = elimina_tildes(servi)
                            ser.append(vicio(servi,servi))
                            apex.append(servi)
                            #print(servi)
                            #aux =[]
                            for alias in servicio.iter('alias'):
                                al = str(alias.text).replace(' ','').lower()
                                al = elimina_tildes(al)
                                #print(al)
                                ser.append(vicio(servi,al))
                                #print(aux)
                            j+=1
                    #print(apex)        
                    #print(empre)
                    #print(repr(ser))
            for lista in Solicitud.iter('lista_mensajes'):
                for mensaje in lista.iter('mensaje'):
                    aux_mensaje = str(mensaje.text).lower()
                    lista_mensaje = aux_mensaje.split(':')
                    aux_mensaje = lista_mensaje[4]
                    aux_mensaje=elimina_tildes(aux_mensaje)
                    print(aux_mensaje)
                    fecha=Lecturafecha(str(mensaje.text))
                    fecha = fecha.replace(' ','')
                    list_fecha.append(fecha)
                    for x in range(len(empre)):

                        hola = re.findall(empre[x],aux_mensaje) 
                        
                        for k in hola:
                            aux_empresa = empre[x]
                            #print('Empresa:',empre[x])
                    for x in range(len(ser)):
                        efe = re.findall(ser[x].alias,aux_mensaje)
                        for z in efe:
                            aux_servicio =ser[x].servicio
                            #print('Servicio:',ser[x].servicio,'Alias:',ser[x].alias)
                        efe = re.findall(ser[x].servicio,aux_mensaje)
                        for z in efe:
                            aux_servicio =ser[x].servicio
                            #print('Servicio:',ser[x].servicio,'Alias:',ser[x].alias)
                    positivo = 0
                    negativo = 0
                    for x in range(len(prueba)):
                        
                        hola = re.findall(prueba[x].palabra,aux_mensaje) 
                        for k in hola:
                            if prueba[x].tipo == 'p':
                                positivo += 1
                            if prueba[x].tipo == 'n':
                                negativo += 1
                    if positivo<negativo:
                        estado = "negativo"
                    elif positivo>negativo:
                        estado = "positivo"
                    elif positivo == negativo:
                        estado = "neutro"
                    ob_men.append(Men(fecha,aux_empresa,aux_servicio,estado))
                print(repr(ob_men))
                    
                    
    except:
        print("Error")
    

def data():
    for bb in list_fecha:
        if bb not in sinrepe:
            sinrepe.append(bb)

    for bb in apex:
        if bb not in nose:
            nose.append(bb)
    print(nose)
    aaa = len(empre)
    aaa2=len(nose)
    for i in range(len(sinrepe)):
        total_fecha=0
        total_positivo = 0
        total_negativo = 0
        total_neutro = 0
        for k in range(len(empre)):
            e_total_fecha=0
            e_total_positivo = 0
            e_total_negativo = 0
            e_total_neutro = 0
            for l in range(len(nose)):
                s_total_fecha=0
                s_total_positivo = 0
                s_total_negativo = 0
                s_total_neutro = 0
                for j in range(len(ob_men)):
                    if ob_men[j].fecha == sinrepe[i]:
                        total_fecha += 1
                        if ob_men[j].estado == 'positivo':
                            total_positivo+=1
                        if ob_men[j].estado == 'negativo':
                            total_negativo+=1
                        if ob_men[j].estado == 'neutro':
                            total_neutro+=1
                    
                        if ob_men[j].empresa == empre[k]:
                            e_total_fecha+=1
                            if ob_men[j].estado == 'positivo':
                                e_total_positivo+=1
                            if ob_men[j].estado == 'negativo':
                                e_total_negativo+=1
                            if ob_men[j].estado == 'neutro':
                                e_total_neutro+=1
                            if ob_men[j].servicio == nose[l]:
                                    s_total_fecha += 1
                                    if ob_men[j].estado == "positivo":
                                        s_total_positivo += 1
                                    if ob_men[j].estado == "negativo":
                                        s_total_negativo += 1
                                    if ob_men[j].estado == "neutro":
                                        s_total_neutro += 1
                if s_total_fecha>0:
                    cantidad_servicio.append(men_servi(sinrepe[i],empre[k],nose[l],s_total_fecha,s_total_positivo,s_total_negativo,s_total_neutro))
                    
            if e_total_fecha>0:      
                cantidad_empresa.append(men_empr(sinrepe[i],empre[k],int(e_total_fecha/aaa2),int(e_total_positivo/aaa2),int(e_total_negativo/aaa2),int(e_total_neutro/aaa2)))
        
        cantidad_mensaje.append(fech(sinrepe[i],int(total_fecha/(aaa*aaa2)),int(total_positivo/(aaa*aaa2)),int(total_negativo/(aaa*aaa2)),int(total_neutro/(aaa*aaa2))))    
    
    
    print(repr(cantidad_servicio))
    print(repr(cantidad_empresa))
    print(repr(cantidad_mensaje))

def ArchivoSalida():
    global ob_men, cantidad_mensaje, cantidad_empresa, cantidad_servicio
    root = ET.Element("lista_respuesta")
    Respuesta = ET.SubElement(root,"respuesta")
    for i in cantidad_mensaje:
        ET.SubElement(Respuesta, "fecha").text = str(i.fecha)
        Mensajes = ET.SubElement(Respuesta,"mensajes")
        ET.SubElement(Mensajes,"total").text = str(i.total)
        ET.SubElement(Mensajes,"positivos").text = str(i.t_positivo)
        ET.SubElement(Mensajes,"negativos").text = str(i.t_negativo)
        ET.SubElement(Mensajes,"neutro").text = str(i.t_neutro)
        Analisis = ET.SubElement(Respuesta,"analisis")
        for j in range(len(cantidad_empresa)):
            if str(i.fecha) == str(cantidad_empresa[j].fecha):
                ET.SubElement(Analisis,"empresa").attrib = {"nombre":cantidad_empresa[j].empresa}
                Mensajes = ET.SubElement(Analisis,"mensajes")
                ET.SubElement(Mensajes,"total").text = str(cantidad_empresa[j].total)
                ET.SubElement(Mensajes,"positivos").text = str(cantidad_empresa[j].t_positivo)
                ET.SubElement(Mensajes,"negativos").text = str(cantidad_empresa[j].t_negativo)
                ET.SubElement(Mensajes,"neutro").text = str(cantidad_empresa[j].t_neutro)
                Servicios = ET.SubElement(Analisis,"servicios")
                for k in range(len(cantidad_servicio)):
                    if str(i.fecha) == str(cantidad_servicio[k].fecha) and str(cantidad_empresa[j].empresa) == str(cantidad_servicio[k].empre):
                        ET.SubElement(Servicios,"servicio").attrib = {"nombre":cantidad_servicio[k].servicio}
                        Mensajes = ET.SubElement(Servicios,"mensajes")
                        ET.SubElement(Mensajes,"total").text = str(cantidad_servicio[k].total)
                        ET.SubElement(Mensajes,"positivos").text = str(cantidad_servicio[k].t_positivo)
                        ET.SubElement(Mensajes,"negativos").text = str(cantidad_servicio[k].t_negativo)
                        ET.SubElement(Mensajes,"neutro").text = str(cantidad_servicio[k].t_neutro)
                    else:
                        None
    def Parseo(elemento, identificador='  '):
        validar = [(0, elemento)]  

        while validar:
            level, elemento = validar.pop(0)
            children = [(level + 1, child) for child in list(elemento)]
            if children:
                elemento.text = '\n' + identificador * (level+1)  
            if validar:
                elemento.tail = '\n' + identificador * validar[0][0]  
            else:
                elemento.tail = '\n' + identificador * (level-1)  
            validar[0:0] = children 

    Parseo(root)
    archio = ET.ElementTree(root) 
    archio.write("./salida.xml", encoding='UTF-8')
    xml_str = ElementTree.tostring(root).decode()
    return xml_str 
from xml.etree import ElementTree   


def LecturaMensaje():
    try:
        xml = request.get_data().decode('utf-8')
        root = ET.XML(xml)
        #root = gestion.getroot()
        for mensaje in root.iter('mensaje'):
            aux_mensaje = str(mensaje.text).lower()
            lista_mensaje = aux_mensaje.split(':')
            nombre = lista_mensaje[3]
            nombre = nombre.split(' ')
            nombre = nombre[1]
            social = lista_mensaje[4]
            social = social.split(' ')
            social = social[1]
            aux_mensaje = lista_mensaje[4]
            aux_mensaje=elimina_tildes(aux_mensaje)
            for i in range(len(empre)):
                hola = re.findall(empre[i],aux_mensaje)
                for k in hola:
                    tipo_empresa =empre[i]
            print(aux_mensaje)
            fecha=Lecturafecha(str(mensaje.text))
            fecha = fecha.replace(' ','')
            positivo = 0
            negativo = 0
            total=0
            for x in range(len(ser)):
                efe = re.findall(ser[x].alias,aux_mensaje)
                for z in efe:
                    tipo_servicio =ser[x].servicio
                efe = re.findall(ser[x].servicio,aux_mensaje)
                for z in efe:
                    tipo_servicio =ser[x].servicio
            for x in range(len(prueba)):
                hola = re.findall(prueba[x].palabra,aux_mensaje) 
                for k in hola:
                    #print(k)
                    total+=1
                    if prueba[x].tipo == 'p':
                        positivo += 1
                    if prueba[x].tipo == 'n':
                        negativo += 1 
            sentimiento_positivo = str(int((positivo*100)/total))
            sentimiento_negativo = str(int((negativo*100)/total))
            if sentimiento_positivo<sentimiento_negativo:
                estado = "negativo"
            elif sentimiento_positivo>sentimiento_negativo:
                estado = "positivo"
            elif sentimiento_positivo == sentimiento_negativo:
                estado = "neutro"
        

            mensaje_corto.append(corto(fecha,social,nombre,tipo_empresa,tipo_servicio,positivo,negativo,(sentimiento_positivo+'%'),(sentimiento_negativo+'%'),estado))
            ob_fecha.append(fecha)
        print(repr(mensaje_corto))
    except:
        print("Error")


def ArchivoSalida2():
    root = ET.Element("respuesta")
    mensaje = ET.SubElement(root,"mensaje")
    for i in mensaje_corto:
        ET.SubElement(mensaje, "fecha").text = str(i.fecha)
        ET.SubElement(mensaje, "red_social").text = str(i.red_social)
        ET.SubElement(mensaje, "usuario").text = str(i.usuario)
        empresaaa = ET.SubElement(mensaje,"empresas")
        ET.SubElement(empresaaa,"empresa").attrib = {"nombre":i.empresa}
        ET.SubElement(empresaaa,"servicio").text = str(i.servicio)
        ET.SubElement(root,"palabras_positivas").text = str(i.t_positivo)
        ET.SubElement(root,"palabras_negativas").text = str(i.t_negativo)
        ET.SubElement(root,"sentimiento_positivo").text = str(i.s_positivo)
        ET.SubElement(root,"sentimiento_negativo").text = str(i.s_positivo)
        ET.SubElement(root,"sentimiento_analizado").text = str(i.s_analizado)
    def Parseo(elemento, identificador='  '):
        validar = [(0, elemento)]  

        while validar:
            level, elemento = validar.pop(0)
            children = [(level + 1, child) for child in list(elemento)]
            if children:
                elemento.text = '\n' + identificador * (level+1)  
            if validar:
                elemento.tail = '\n' + identificador * validar[0][0]  
            else:
                elemento.tail = '\n' + identificador * (level-1)  
            validar[0:0] = children 

    Parseo(root)
    archio = ET.ElementTree(root) 
    archio.write("./salidamen.xml", encoding='UTF-8')
    xml_str = ElementTree.tostring(root).decode()
    return xml_str 


def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD',cadena) if unicodedata.category(c) != 'Mn'))
    return s

def Lecturafecha(fecha):
    try:
        fecha  = re.search(r'\d{2}(\/)\d{2}(\/)\d{4}',fecha)
        return fecha.group()
        
    except:
        return 'NoSeEncontro'

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

@app.route('/crearsalida', methods=['POST'])
def post_events():
    dataRquestesd = request.data.decode('iso-8859-1')
    
    data = open('datos.xml', 'w')
    data.write(dataRquestesd)
    data.close()
    LecturaDatos()
    return jsonify({'ok' : True, 'msg':'Archivo XML leído correctamente'}), 200

@app.route('/getsalida', methods=['GET'])
def get_events():
    data()
    dataa = ArchivoSalida()
    return Response(response=dataa)


@app.route('/mandarmensaje', methods=['POST'])
def post_events1():
    dataRquestesd1 = request.data.decode('iso-8859-1')
    
    data1 = open('mensaje.xml', 'w')
    data1.write(dataRquestesd1)
    data1.close()
    LecturaMensaje()
    return jsonify({'ok' : True, 'msg':'Mensaje xml enviado correctamente'}), 200

@app.route('/getsalidamensaje', methods=['GET'])
def get_events2():
    dataa1 = ArchivoSalida2()
    return Response(response=dataa1)

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
    global listapalabrasn, listapalabras, prueba, ob_fecha, otro, empre, ser, ob_men
    global list_fecha, sinrepe, aux_c_servicios, cantidad_servicio, cantidad_mensaje, cantidad_empresa
    global nose, apex, mensaje_corto
    listapalabras = []
    listapalabrasn = []
    prueba = []
    ob_fecha=[]
    otro = []
    empre = []
    ser =[]
    ob_men=[]
    list_fecha=[]
    sinrepe=[]
    aux_c_servicios=[]
    cantidad_mensaje=[]
    cantidad_empresa=[]
    cantidad_servicio=[]
    nose=[]
    apex=[]
    mensaje_corto = []
    fo = open("salida.xml","w")
    fo.write("")
    fo.close()
    respuesta = {
        'mensaje' : 'Base reseteada'
    }
    return jsonify(respuesta)

    
def ResumenEmpresafecha(fecha,empresa):
    fechaNew = LecturafechaEntrada(fecha)
    fechaNew = fechaNew.replace(" ","")
    empresa = empresa.replace(" ","")

    total_empresa= 0
    total_positivo = 0
    total_negativo = 0
    total_neutro = 0

    validacion = False
    
    for i in cantidad_servicio:
        if i.fecha == fechaNew:
            if empresa == i.empre:
                total_empresa += i.total
                total_positivo += i.t_positivo
                total_negativo += i.t_negativo
                total_neutro += i.t_neutro
                validacion = True
            elif empresa == 'todas':
                for x in cantidad_servicio:
                    if x.fecha == fechaNew:
                        total_empresa += x.total
                        total_positivo += x.t_positivo
                        total_negativo += x.t_negativo
                        total_neutro += x.t_neutro
                        validacion = True
            break
            
    
    if validacion:
        text = "Fecha: " + str(fechaNew) + "\nEmpresa: " + str(empresa) + "\nTotal Empresa: " + str(total_empresa)+ "\nMensajes Positivos: " + str(total_positivo)+ "\nMensajes Negativos: " + str(total_negativo)+ "\nMensajes Neutros: " + str(total_neutro)
    else:
        text = "No se encontro Fecha o Empresa indicada"
    
    return text


def LecturafechaEntrada(fecha):

    try:
        fechas = ""
        arreglo = fecha.split("-")
        arreglo.reverse()
        for i in arreglo:
            fechas += i
            if len(i) == 4:
               pass
            else:
                fechas += "/"
        return fechas
        
    except:
        return 'NoSeEncontro'



@app.route ("/resumen_Fecha", methods=['POST'])
def resume_Fecha():
    fecha = request.json['date']
    empresa = request.json['empresa']
    response =  ResumenEmpresafecha(fecha,empresa)
    respuesta = jsonify ({"error": False, "mensaje": response})
    return (respuesta)
        

@app.route('/crearsalida', methods=['GET'])
def crearsalida():
    LecturaDatos()
    data()
    ArchivoSalida()


if __name__=='__main__':
    app.run(debug=True, port=4000)
    