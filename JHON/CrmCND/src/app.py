
#from crypt import methods
from logging.config import dictConfig
from os import curdir
import os
import sys
import json
import time
import threading
from telnetlib import PRAGMA_HEARTBEAT
from traceback import print_tb
import datetime
import flask
import flask_login
import random
import requests


from flask import Flask,render_template,request,redirect,url_for,flash,jsonify,send_file,send_from_directory
from flask_mysqldb import MySQL
from config import config
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from decimal import *

from waitress import serve
from flask_socketio import SocketIO,send,emit, join_room, leave_room

#modelos
from models.Cryp import GestorEnccycode
from models.ModelUser import ModelUser
from models.entities.User import User
from models.ModeloEvaluacion import CalNotaEva,createcsvrespuestas, InformesMasivo
from models.lectorExcel import Lector,MakeInf,generarInformeCsv
from models.modeloCarpetas import CreadorCarpetas
from models.callApi import ConsultorApi

from models.ModelBots import ModelBots
from models.ModeloIntercambioFiles import HandleFiles
from models.entities.Bots import Bot
from models.ConvertidorTimer import Trazador
from models.ModeloItemsMon import ModelConsultas
from models.Matematico import CalNotaMon,CalNotaMonHp, ExtDataDic
#actualizacion 02/05/2024
from models.ConnMysqlBot import ConectorDbMysql

from models.tsck import Handledbmongo,HandleNotificaciones,replace_nan_with_none
from models.modulosshmongo.main  import GestorConsultasshMongo
import re
from ConfAdd import *



app=Flask(__name__)
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=60)
print('inicia')
csrf = CSRFProtect()

RUTAlOCAL= os.path.dirname(os.path.abspath(__file__))
PATHINSTANCE=os.path.dirname(os.path.abspath(__file__))
PATHINSTANCE =os.path.join(PATHINSTANCE,'instance')

os.makedirs(os.path.join(app.instance_path, 'Uploads'), exist_ok=True)
os.makedirs(os.path.join(app.static_folder, 'ImgEvaluaciones'), exist_ok=True)
os.makedirs(os.path.join(app.instance_path, 'UploadsPreturnos'), exist_ok=True)
os.makedirs(os.path.join(app.instance_path, 'RepositorioClaro'), exist_ok=True)
os.makedirs(os.path.join(PATHINSTANCE, 'UploadBacklog'), exist_ok=True)
os.makedirs(os.path.join(PATHINSTANCE, 'Tempdownloads'), exist_ok=True)
os.makedirs(os.path.join(PATHINSTANCE, 'Tempservcali'), exist_ok=True)

db=MySQL(app)
#socketio = SocketIO(app)


login_manager_app = LoginManager(app)
app.config['PREFERRED_URL_SCHEME'] = 'https'


diccolavancebyciudad = {"Bogota": "Avance_operacion_Bogota","Bucaramanga":"Avance_operacion_Bucaramanga",
                                    "Cali":"Avance_operacion_Cali"}

def eliminarAcentos(string):
    return string.translate(string.maketrans("áàäéèëíìïòóöùúüÀÁÄÈÉËÌÍÏÒÓÖÙÚÜ", "aaaeeeiiiooouuuAAAEEEIIIOOOUUU"))

def IsLogeado(usuario):
    if usuario.is_authenticated:
        return True
    else:
        return redirect(url_for('login'))

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.Get_by_id(db,id)


"""
Enable CORS. Disable it if you don't need CORS
https://parzibyte.me/blog
"""
@app.before_request
def before_request():
    flask.session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=60)
    flask.session.modified = True
    flask.g.user = flask_login.current_user


@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*" # <- You can change "*" for a domain for example "http://localhost"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':        
        user=User(0,request.form['username'],request.form['password'])
        logged_user=ModelUser.login(db,user)
        if logged_user!=None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('DashboardCND'))
            else:
                flash("Contraseña incorrecta...")
                return render_template('auth/login.html')
        else:
            flash("Usuario no encontrado...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/DashboardCND')
@login_required
def DashboardCND():
    return render_template('home2.html')

@app.route("/Evaluaciones/<idpreturno>/<idAsesor>")
@login_required
def Evaluaciones(idpreturno,idAsesor):        
    # 1 validar que exista preturno habilitado     1 ok
    # 2 validar que el usuario este con asistencia 1 ok
    # 3 validar que el usuario no tenga evaluacion marcada
    Arraydatos0 = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1,
                                          "procedimiento": "spr_get_estevaase","arraydatos":[idpreturno,idAsesor]})

    if Arraydatos0!=None and Arraydatos0[1]==1 and Arraydatos0[2] == None : # valida que el formador halla habilitado la asistencia
        Arraydatos = ConsultorApi().FuncUpdGetSpr({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1, "procedimiento":
                                                    "spr_get_evapre","arraydatos":[idpreturno,idAsesor]})
        # si el usuario no ha realizado preturno
        IdAsistencia = Arraydatos0[0]

        if Arraydatos[0]!=0:
            ArrayPreguntas=json.loads(Arraydatos[1])
            # funcion experimental randon respuestas
            for dic in ArrayPreguntas:
                for i,j in dic.items():
                    mi_diccionario = j['ResPre']
                    claves_aleatorias = list(mi_diccionario.keys())
                    random.shuffle(claves_aleatorias)
                    diccionario_aleatorio = {clave: mi_diccionario[clave] for clave in claves_aleatorias}
                    j['ResPre'] =diccionario_aleatorio

            return render_template('EleFormacion/evaluacion.html',IdEvaluacion=Arraydatos[0],idNumerario=IdAsistencia,ArrayPreguntas=ArrayPreguntas)
        else:
            return render_template("/EleFormacion/vistapreturnos.html")

    else:
        return render_template("/EleFormacion/vistapreturnos.html")

#background process happening without any refreshing
@app.route('/GetDataAseMOn',methods=['POST'])
@login_required
def GetDataAseMOn():
    JsonOption = request.get_json()
    data=ModelUser.getDatAseMon(db,JsonOption['cedula'])
    if data==None:
        data=[None,None,None,None,None,None]
    else:
        pass
    return json.dumps({'Nombre' : data[0],'Proceso':data[1],'Estado':data[2],'cordinador':data[3],'fechIngreso':str(data[4]),'formador':data[5]})

#Consulta los datos del formulario
@app.route('/GetDataFormMon',methods=['POST','GET'])
@login_required
def GetDataFormMon():        
    Camp =request.get_json()    
    data=ModelConsultas.GetDataFormMon(db,Camp['Campaña'])
    if data==None:
        data=[None,None,None,None,None,None]
    else:
        pass

    #x=jsonify({'DicDatForm': data})

    return json.dumps({'DicDatForm': data}, default=str)
     

@app.route('/CalcNotaMon',methods=['POST'])
@login_required
def CalcNotaMon():      
    DicDatosFor = request.get_json()
    if DicDatosFor['Segmento']=="HOGAR":
        res = json.loads(DicDatosFor['DatoForm'])    
        ArrayNotas=CalNotaMon(res)
        return json.dumps({'TotalCrit':round(float(ArrayNotas[0]),1),'TotalNoCritico':round(float(ArrayNotas[1]),1),
                           'SumaCritico':round(float(ArrayNotas[0]),1),'NotaTotal' : round(float(ArrayNotas[2]),1),'ItemsAfec':round(ArrayNotas[0],1)})
    else:
        res = json.loads(DicDatosFor['DatoForm'])    
        ArrayNotas=CalNotaMonHp(res)        
        return json.dumps({'TotalCrit':float(ArrayNotas[0]),'TotalNoCritico':float(ArrayNotas[1]),'SumaCritico':float(ArrayNotas[0]),'NotaTotal' : float(ArrayNotas[2]),'ItemsAfec':ArrayNotas[0]})
        
        
@app.route('/updgestionMon', methods=['POST'])
@login_required
def updgestionMon():
    ArrayDatosForMon = request.form.get('DatoMon')
    res = json.loads(ArrayDatosForMon)
    NumeroRad=ModelConsultas.InsDataForm(db,ExtDataDic(res))
    del res, ArrayDatosForMon
    return jsonify({"RadMonitoreo":NumeroRad})

@app.route('/UpdMuesta', methods=['POST'])
@login_required
def UpdMuesta():
    JsonOption = request.get_json()
    dicNotas = {"Items": JsonOption['JsonCaliItems']}
    if JsonOption['Segmento'] == "HHPP":
        ArrayNotas = CalNotaMonHp(dicNotas)
    else:
        ArrayNotas = CalNotaMon(dicNotas)
    JsonOption.pop('Segmento')
    JsonOption.pop('JsonCaliItems')
    ArrayValors = list(JsonOption.values())
    ArrayValors.append(ArrayNotas[2])
    ArrayValors.append(ArrayNotas[1])
    ArrayValors.append(ArrayNotas[0])
    ArrayValors.append(ArrayNotas[1])

    ModelConsultas.FuncionUpdDelSpr(db, ["spr_upd_mon", ArrayValors])
    for i in dicNotas.values():
        for j in i:
            ModelConsultas.FuncionUpdDelSpr(db, ["spr_upd_calmon",
                                                 [JsonOption['IdMuestra'], j['IdItem'], j['Calificacion']]])
    return ("", 204)



@app.route("/lectorxml", methods=["GET","POST"])
@login_required
def lectorxml():
    if request.method == 'POST':
        file = request.files['upload-file']
        Idasecalidad=request.form["idcalidad"]
        if file.filename!="":
            #if " "in file.filename:
            #file.filename = file.filename.replace(" ", "_")
            #flash("Nombre del archivo cargado no valido, favor cambielo!")
            #return redirect("/UploadMonClaro")
            pathFile =os.path.join(app.instance_path, 'Uploads', secure_filename(file.filename))
            file.save(pathFile)
            try:
                ArrayDatoExcel=Lector.BigDataMonitoreoClaro(pathFile)
            except Exception as e:
                flash("Error con el archivo escogido "+str(e))
                return redirect("/UploadMonClaro")

            for i in ArrayDatoExcel:
                LoginAse=i['DatosMon']['Login']
                sql=f"select usu_nid from tbl_husuarioscrm where usu_nlogin='{LoginAse}'"                          
                query=ModelConsultas.FuncionSel(db,[sql])
                if len(query)==0:
                    continue
                else:
                    for cedula in query[0]:
                        Idreg = ModelConsultas.InsCargaClaro(db,
                        [cedula, Idasecalidad, i['DatosMon']['Aliado'], "Claro",
                        "Claro", i['DatosMon']['TipoOrden'], "Monitoreo Claro",
                        i["DatosMon"]["FechaMon"], i["DatosMon"]["Cuenta"],
                        i["DatosMon"]["Orden"], i["DatosMon"]["fechaAge"],
                        i["DatosMon"]["TipoOrden"],
                        i["DatosMon"]["Orden"], i["DatosMon"]["Razon"], "Na",
                        i["DatosMon"]["Observaciones"],
                        i["DatosMon"]["Nota"], i["DatosMon"]["Nec"],
                        i["DatosMon"]["Nenc"], i["DatosMon"]["Nerrores"]])
                        ## CARGAR LOS ITEMS
                        ModelConsultas.CargaItemsClaro(db,i['DatosItems'],Idreg,cedula)
                        
            flash("Archivo cargado con exito")
        else:
            flash("Cargue un archivo en el formato indicado!")
            
    return redirect("/UploadMonClaro")

@app.route("/lectorXLSform", methods=["GET","POST"])
@login_required
def lectorXLSform():    
    if request.method == 'POST':
        file = request.files['upload-file']
        IdaseForm=request.form["idAseForm"]   
        IdPreturno=request.form["idPreForm"]
        file.filename = eliminarAcentos(file.filename)
        if file.filename!="":
            if " " in file.filename:
                file.filename=file.filename.replace(" ","_")
            #for i in re.findall(r'\W', file.filename):
            #    file.filename=file.filename.replace(i,"_")

            file.save(os.path.join(app.instance_path, 'Uploads', secure_filename(file.filename)))
            filexls=str(os.path.join(app.instance_path, 'Uploads', file.filename))
            #try:
            Lector.LectorNotasPreturno(db,IdPreturno,IdaseForm,filexls)
            '''except Exception as e:
                flash("Error con el archivo escogido "+str(e))
                return redirect("/UploadMonClaro")'''
    flash("Preturno cargado con exito!!!")
    return redirect(url_for("Enrrutador",application_name="SubirPreturno"))


@app.route("/CreacionUser")
@login_required
def CreacionUser():    
    query=ModelConsultas.FuncionGetSPR(db,["SPR_GET_SUPACT"])    
    dictDatoCreacion={
        "CAMPAÑA":[dato[0] for dato in query if dato[1]=="CampañaAsesor" ],
        "CARGO":[dato[0] for dato in query if dato[1]=="CargoAsesor"],
        "PERFIL":[dato[0] for dato in query if dato[1]=="PerfilAsesor"],
        "CIUDAD":[dato[0] for dato in query if dato[1]=="CiudadAsesor"],
        "SUPERVISOR":[dato[0] for dato in query if dato[1]=="SupervisorAsesor"]}
    
    return render_template("EleAdmin/CreacionUser.html",dictDatos=dictDatoCreacion)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


#######################
'''contador=0
ArrayRangos=[]
for i in range(6,22):
    for j in range(2):
        if j==0:
           ArrayRangos.append(f"{str(i).zfill(2)}:{str(contador).zfill(2)} a {str(i).zfill(2)}:{contador+30}")
        elif j==1:
            ArrayRangos.append(f"{str(i).zfill(2)}:{str(int(contador+30)).zfill(2)} a {str(int(i+1)).zfill(2)}:{str(contador).zfill(2)}")'''


@app.route('/SelectInteractivos',methods=["GET","POST"])
def SelectInteractivos():
    JsonOption = request.get_json()

    if JsonOption['Proceso'] in [ "HHPP"]:
        return json.dumps({"TIPOORDEN":["Creación Hhpp Bidireccional","Cambio De Dirección Hhpp","Creación Hhpp Mer",
                "Modificación Cm / Mer","Cambio Estrato Suscriptor","Creación Cm","Creación Hhpp En Cm","Modificar Eliminar Cm / Mgl",
                "Cambio Estrato Cm","Reactivación Hhpp","Fichas"
                ],"RAZONES":[
                        "BARRIO DUPLICADO EN LA SOLICITUD",
                        "CAMBIO DE DIRECCION NO REALIZADO",
                        "CAMBIO DE DIRECCION REALIZADO",
                        "CARACTER NO VALIDO EN UNIDAD A MODIFICAR",
                        "CONFIRMAR DISTRIBUCION DE HHPP EXISTENTE",
                        "DATOS DE DIRECCION INCOMPLETOS",
                        "DIRECCION ASOCIADA A CUENTA MATRIZ",
                        "FUERA DE ZONA",
                        "GESTION DE HHPP DE FORMA MANUAL",
                        "HHPP ACTUALIZADO",
                        "HHPP CREADO",
                        "HHPP EN USO POR OTRO USUARIO",
                        "HHPP YA EXISTE EN RR",
                        "NO SE CREAN HHPP EN NODO APAGADO",
                        "REACTIVACION HHPP NO REALIZADO",
                        "REACTIVACION HHPP REALIZADO",
                        "SOLICITAR POR EL LINK MGL",
                        "SOLICITUD MAL REALIZADA",
                        "VERIFICACION AGENDANDA",
                        "CUENTA MATRIZ CREADA",
                        "CUENTA MATRIZ CON O SIN VT NO SE CREA EL HHPP",
                        "CAMBIO DE ESTRATO REALIZADO",
                        "CUENTA MATRIZ ACTUALIZADA",
                        "SOLICITUD REPETIDA",
                        "CUENTA MATRIZ YA EXISTE EN RR",
                        "CUENTA MATRIZ CREADA",
                        "NO SE PUBLICO DOCUMENTO DE SOPORTE",
                        "GESTION REALIZADA",
                        "BARRIO DUPLICADO EN LA SOLICITUD",
                        "SOPORTE NO VALIDO",
                        "SOPORTE NO SE DEJA VISUALIZAR",
                        "SOPORTE CON ENMENDADURA",
                        "HHPP CON OT ABIERTA",
                        "CAMBIO DE ESTRATO YA EXISTE EN RR",
                        "DIRECCION INCOMPLETA",
                        "HHPP CREADOS",
                        "NO HAY PUBLICACION DE VT",
                        "HHPP HABILITADO",
                        "CUENTA MATRIZ ELIMINADA",
                        "VERIFICACION AGENDADA",
                        "CAMBIO DE NODO REALIZADO",
                        "RECHAZAR ELIMINACION CM",
                        ]}
                        )        
    else:
        return json.dumps({"TIPOORDEN": ["Arreglo", "Blindaje", "Brownfield", "Instalacion", "postventa", "Traslado"],
                           "RAZONES": ["B - DIRECCION Y/O DATOS ERRADOS",
                                       "C - NO CONTACTO CON EL CLIENTE",
                                       "E - SUSCRIPTOR NO DESEA/NO REQUIERE TRABAJOS",
                                       "F - FALTA DE MATERIALES/EQUIPOS CLARO",
                                       "H - REQUIERE AMPLIACIÓN DE PUERTOS",
                                       "I - INCUMPLIMIENTO ALIADO",
                                       "K - CLIENTE SOLICITA REPROGRAMAR",
                                       "L - LLUVIA - FACTORES CLIMÁTICOS",
                                       "M - MAL AGENDADO/MAL PROGRAMADO",
                                       "N - ESCALAMIENTO NOC",
                                       "O - CLIENTE NO TIENE DINERO",
                                       "P - PERMISOS DE ADMINISTRACION",
                                       "Q - PROBLEMAS EN SISTEMAS-APLICATIVOS CLARO",
                                       "R - REPLANTEAMIENTO VT",
                                       "S - NO INGRESO/CLIENTE CONFIRMA SERVICIO OK",
                                       "V - UNIDAD POSIBLE FRAUDE",
                                       "W - DUCTOS/INFRESTRUCTURA PREDIO NO APTA",
                                       "X - PROBLEMA ORDEN PUBLICO/ZONA ROJA",
                                       "Y - INSTALACIÓN REQUIERE ANDAMIO-ARNES",
                                       "Z - FUERA ZONA/ SIN COBERTURA RED",
                                       "4 - VENTA DEVUELTA AL ASESOR",
                                       "5 - PROBLEMA TARIFA/SERVICIOS DIGITADO",
                                       "6 - EQUIPOS CLIENTE NO APTOS/NO DISPONIBLES",
                                       "7 - CLIENTE AUN NO DESEA EL TRABAJO",
                                       "? - SUSCRIPTOR NO ESTA EN CONDICIÓN DE ATENDER",
                                       "(+) - CAMARA/SOLDADA O INUNDADA",
                                       "(=) - REQUIERE MOVIL ELITE",
                                       "/ - FUERA DE COBERTURA WTTH",
                                       "@ - ESCALAMIENTO NOC @",
                                       "# - ESCALAMIENTO NOC TV",
                                       "$ - ESCALAMIENTO NOC TELEFONIA",
                                       "'%' - ESCALAMIENTO NOC RED BI",
                                       "& - ESCALAMIENTO NOC PYMES",
                                       "GESTION BACKLOG",
                                       "MINTIC",
                                       "CONFIRMACION",
                                       "ENRUTAMIENTO",
                                       "VISITA OK FO"]})


DicDatos={
    "CND":["CENTRO","MEC","OCCIDENTE","ORIENTE"],
    "CUENTA":"Claro CND BOGOTA",
    "CIUDAD":["BOGOTA","CALI","BUCARAMANGA"],
    "AREAMON":["CALIDAD","Claro","MEC","SUPERVISOR","FORMACION"],
    "AUDITOR":[
        {"NombreAud":"JOAN CAMILO SERRANO CHAVEZ","CedAud":1022955073,"Cnd":"CENTRO","Area":"CALIDAD"},
        {"NombreAud":"MILTON GIOVANNI TIRIA CORREDOR","CedAud":1012370702,"Cnd":"CENTRO","Area":"CALIDAD"},
        {"NombreAud":"SONIA LISBETH SAAVEDRA RAMIREZ","CedAud":1015430024,"Cnd":"CENTRO","Area":"CALIDAD"},
        {"NombreAud":"MANUEL FABIAN USECHE HENAO","CedAud":1026290405,"Cnd":"CENTRO","Area":"FORMACION"},
        {"NombreAud":"MEC","CedAud":"MEC","Cnd":"MEC","Area":"MEC"},
        {"NombreAud":"JEFFREY ARLEX GARCIA ARARTH","CedAud":1144025554,"Cnd":"CENTRO","Area":"CALIDAD"},
        {"NombreAud":"SANDRA ASTRID FERNANDEZ GAMEZ","CedAud":1013605963,"Cnd":"CENTRO","Area":"SUPERVISOR"},
        {"NombreAud":"LUZ ADRIANA RESTREPO ROA","CedAud":52846414,"Cnd":"CENTRO","Area":"SUPERVISOR"},        
        {"NombreAud":"SANTIAGO ALEJANDRO GARCIA MARTINEZ","CedAud":1022411312,"Cnd":"CENTRO","Area":"SUPERVISOR"},
        {"NombreAud":"SONIA LISBETH SAAVEDRA RAMIREZ","CedAud":1015430024,"Cnd":"CENTRO","Area":"SUPERVISOR"},
        {"NombreAud":"Dominguez Vergara Orlando","CedAud": 16932909,"Cnd":"OCCIDENTE","Area":"SUPERVISOR"}, 
        {"NombreAud":"Martinez Giraldo Leydi Johana","CedAud": 52979707,"Cnd":"OCCIDENTE","Area":"SUPERVISOR"}, 
        {"NombreAud":"Botero Franco Leived","CedAud": 1144138849,"Cnd":"OCCIDENTE","Area":"SUPERVISOR"},    
        {"NombreAud":"Davalos Botero Christian Andres","CedAud": 1144154708,"Cnd":"OCCIDENTE","Area":"SUPERVISOR"}, 
        {"NombreAud":"Sinisterra Castro Carlos Duban","CedAud": 1144192146,"Cnd":"OCCIDENTE","Area":"SUPERVISOR"},
        {"NombreAud":"Joaquín Quinayas Edwin Fabian","CedAud": 1061810538,"Cnd":"OCCIDENTE","Area":"SUPERVISOR"},
        {"NombreAud":"Romero Velez Yerli Jannin","CedAud": 1143982244,"Cnd":"OCCIDENTE","Area":"SUPERVISOR"},
        {"NombreAud":"Lopez Murillo Luz Catherine","CedAud":29689116    ,"Cnd":"OCCIDENTE","Area":"CALIDAD"},
        {"NombreAud":"Fernandez Jaramillo Lina Fernanda","CedAud":1107089960,"Cnd":"OCCIDENTE","Area":"CALIDAD"},
        {"NombreAud":"Peña Guzman Ingrid Johana","CedAud":1143842856   ,"Cnd":"OCCIDENTE","Area":"FORMACION"},
        {"NombreAud":"Borrero Martinez Marien Dayanna","CedAud":1143870888  ,"Cnd":"OCCIDENTE","Area":"FORMACION"}
        ],
    "TIPOAUD":["MUESTRA","REMOTO","LADO A LADO","PANTALLA"],
    "PORCESO":["DESPACHO","BACKLOG","HHPP"],
    "CUMPLIMIENTO":['Cumple','No cumple'],
    "COMODINTO":["Arreglo","Blindaje","Brownfield","Intalacion","Postventa","Traslado"],
    "COMODIN1":["B - DIRECCION Y/O DATOS ERRADOS",
                "C - NO CONTACTO CON EL CLIENTE",
                "E - SUSCRIPTOR NO DESEA/NO REQUIERE TRABAJOS",
                "F - FALTA DE MATERIALES/EQUIPOS CLARO",
                "H - REQUIERE AMPLIACIÓN DE PUERTOS",
                "I - INCUMPLIMIENTO ALIADO",
                "K - CLIENTE SOLICITA REPROGRAMAR",
                "L - LLUVIA - FACTORES CLIMÁTICOS",
                "M - MAL AGENDADO/MAL PROGRAMADO",
                "N - ESCALAMIENTO NOC",
                "O - CLIENTE NO TIENE DINERO",
                "P - PERMISOS DE ADMINISTRACION",
                "Q - PROBLEMAS EN SISTEMAS-APLICATIVOS CLARO",
                "R - REPLANTEAMIENTO VT",
                "S - NO INGRESO/CLIENTE CONFIRMA SERVICIO OK",
                "V - UNIDAD POSIBLE FRAUDE",
                "W - DUCTOS/INFRESTRUCTURA PREDIO NO APTA",
                "X - PROBLEMA ORDEN PUBLICO/ZONA ROJA",
                "Y - INSTALACIÓN REQUIERE ANDAMIO-ARNES",
                "Z - FUERA ZONA/ SIN COBERTURA RED",
                "4 - VENTA DEVUELTA AL ASESOR",
                "5 - PROBLEMA TARIFA/SERVICIOS DIGITADO",
                "6 - EQUIPOS CLIENTE NO APTOS/NO DISPONIBLES",
                "7 - CLIENTE AUN NO DESEA EL TRABAJO",
                "? - SUSCRIPTOR NO ESTA EN CONDICIÓN DE ATENDER",
                "(+) - CAMARA/SOLDADA O INUNDADA",
                "(=) - REQUIERE MOVIL ELITE",
                "/ - FUERA DE COBERTURA WTTH",
                "@ - ESCALAMIENTO NOC @",
                "# - ESCALAMIENTO NOC TV",
                "$ - ESCALAMIENTO NOC TELEFONIA",
                "'%' - ESCALAMIENTO NOC RED BI",
                "& - ESCALAMIENTO NOC PYMES",
                "GESTION BACKLOG",
                "MINTIC",
                "CONFIRMACION",
                "ENRUTAMIENTO",
                "VISITA OK FO"],
    "COMODIN2":[1,2,3,4,5,"N/A"],
    #"Tiempos":ArrayRangos
}



#rutas protegidas sidebar
@app.route("/PlaDespachos")
@login_required
def PlaDespachos():
    Dicoptcancelar = {"TipoOt": {"Lls": {"Señal ok mal agendado": "LSC", "Incidente": "n04"}, "Ots": {"Direccion": "13",
                                                                                                      "Mal agendada": "06",
                                                                                                      "Fuera de zona": "03",
                                                                                                      "Sus no desea servicio": "09",
                                                                                                      "Unidad posible fraude": "21",
                                                                                                      "Venta devuelta": "04"}},
                      "Gestiones": ["Enviar a completar", "Enviar a cancelar"], "codCierre": ["LSC", "N04"]}
    return render_template('EleGestion/PlantillasDes.html',opcionesVista=DicOpciones,Dicoptcancelar=Dicoptcancelar)




@app.route('/NuevoMonitoreo')
@login_required
def NuevoMonitoreo():
        query=ModelConsultas.FuncionGetSPR(db,["spr_get_staff"])
        return render_template('EleCalidad/formEvaluador.html',DicDatForm=DicDatos,Perfiles=query)

@app.route('/EditarMonitoreo')
@login_required
def EditarMonitoreo():
        query=ModelConsultas.FuncionGetSPR(db,["spr_get_staff"])
        return render_template('EleCalidad/FromEditarMon.html',DicDatForm=DicDatos,Perfiles=query)#, arrayGestionH=ArrayCasos)


@app.route('/UploadMonClaro')
@login_required
def UploadMonClaro():
    return render_template('EleCalidad/CargaMonClaro.html')

#rutas protegidas
@app.route('/HistorialMon/<character_id>', methods=['GET', 'POST'])
@login_required
def HistorialMon(character_id):
    ArrayCasos= ModelConsultas.GetDataCasoHis(db,character_id)
    return render_template('EleCalidad/HistorialMonitoreos.html', arrayGestionH=ArrayCasos)

@app.route('/DetCaso',methods=['POST','GET'])
@login_required
def DetCaso():
    IDCaso = request.get_json()
    ArrayCasos= ModelConsultas.GetDetMon(db,IDCaso['Caso'])
    ArrayItems=ModelConsultas.GetIteMon(db,IDCaso['Caso'])
    ArraySol=ModelConsultas.FuncionGetSPR(db,["spr_get_solicaso",IDCaso['Caso']])
    
    sql="select distinct(smo_cid) from  tbl_hsolicitudesmon where smo_cidmon='"+str(IDCaso['Caso'])+"'"    
    dicResCasos={}
    for i in ModelConsultas.FuncionSel(db,[sql]):        
        ArrayRepuestas=[]
        for j in ModelConsultas.FuncionGetSPR(db,["spr_get_rescasos",i[0]]):                           
            ArrayRepuestas.append(list(j))
        dicResCasos.update({i[0]:ArrayRepuestas})

    dic={}
    for i,j in enumerate(ArrayCasos):
        dic.update({str(i).zfill(2):str(j)})
    dic.update({'items':ArrayItems})
    dic.update({'Solicitudes':ArraySol})
    dic.update({'RepuestasSol':dicResCasos})
    return json.dumps(dic)


##################vistas del orquestador#####################

@app.route('/VistaBotsGes')
@login_required
def VistaBotsGes():
    DicBots=ModelBots.GetAllBots(db)
    DicGen={"Backoffice":[1,2,3],
            "Labor":["Crear","Completar","Marcar Confirmacion","Marcar Demora","Marcar Seguimiento","Marcacion Soporte","Marcacion TAM","Marcacion Multiple","Repara y Actualiza","Actualizar","Marcacion MiN & PY"],
            "Ciudad":["Bogota","Cali"]}
    return render_template('EleOrquestador/ListadoBots.html',DicBotsActivos=DicBots,DicDatOrq=DicDatos)


@app.route('/VistaBotsInformes')
@login_required
def VistaBotsInformes():
    return render_template('EleOrquestador/InformesBots.html')


@app.route('/GetProgressBot',methods=['POST'])
@login_required
def GetProgressBot():
    NomBot = request.get_json()
    if NomBot['LaborBot'] == "Completar":
        TipConsulta = "SPR_GET_DETGESCOM"
    elif NomBot['LaborBot']== "Crear":
        TipConsulta = "SPR_GET_DETGESCRE"
    elif NomBot['LaborBot'] in ['Marcar Demora', 'Marcar Confirmacion', 'Marcacion TAM', 'Marcar Seguimiento',
                              'Marcacion Multiple', 'Marcacion Soporte']:
        TipConsulta = "SPR_GET_DETGESMAR"
    elif NomBot['LaborBot'] in ['Actualizar', 'Repara y Actualiza']:
        TipConsulta = "SPR_GET_DETGESVAL"
    data = ModelConsultas.FuncionGetSPR(db,(TipConsulta,NomBot['NameBot'],))

    _total = int(data[1][0])
    _pendiente = int(data[2][0])
    _Gestionado = int(data[3][0])
    del data,TipConsulta,NomBot
    PorcAvance=round(_Gestionado/_total*100)

    dic={"total":_total,"pendiente":_pendiente,"Gestionado":_Gestionado,"porcentava":PorcAvance}
    del _total,_pendiente,_Gestionado
    return jsonify(dic)

@app.route("/sendrazonasesor",methods=['POST'])
@login_required
def UpdDatarazcan():
    tipoorden = request.form['selTiporden']
    # codcieorden = request.form['selcodcierre']
    numorden = request.form['inporden']
    checkinc = 1 if request.form.get('chkinc') == "1" else 0
    numinc = request.form['inpinc'] if checkinc == "1" else 0
    notorden = request.form['txtnotascan']
    # return ("",204)
    ConsultorApi().callUpd({'servicio': 'BotServer', 'ciudad': dicCiudad[current_user.ciudad], "tipo": 1,
                            "procedimiento": "spr_ins_canordase", "arraydatos":
                                [current_user.id, tipoorden, numorden, checkinc, numinc, notorden, ]})

    return redirect("PlaDespachos")


@app.route("/AppDataBase",methods=['POST'])
@login_required
def AppDataBase():
    JsonOption = request.get_json()    
    if JsonOption['Gestion']=="UpdEstadoBot":
        ModelConsultas.FuncionUpdDel(db,["UPDATE tbl_controlbot SET CTL_CDETALLE1='"+str(JsonOption['NueEstatus'])+"' WHERE CTL_CNOMBOT='"+str(JsonOption['Bot'])+"'"])
        ModelConsultas.FuncionSel(db,["select CTL_CDETALLE1 from tbl_controlbot WHERE CTL_CNOMBOT='"+str(JsonOption['Bot'])+"'"])

    elif JsonOption['Gestion']=="GetDatCaso":
        DetCaso = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1,
                                          "procedimiento": "SPR_GET_INFOFORMCASO",
                                          "arraydatos": [int(JsonOption['CasoBuscar'])
                                                         ]})

        if DetCaso != None:
            if DetCaso[3] == "HHPP":
                NotasCaso = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 2,
                                                    "procedimiento": "SPR_GET_NOTFORMMONHP",
                                                    "arraydatos": [JsonOption['CasoBuscar']
                                                                   ]})

            else:
                NotasCaso = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 2,
                                                    "procedimiento": "SPR_GET_NOTFORMMONCASO",
                                                    "arraydatos": [JsonOption['CasoBuscar']
                                                                   ]})
            dic = {"DataForm": DetCaso, "DataEvaluador": list(NotasCaso)}
        else:
            dic={"DataForm":0,"DataEvaluador":0}

        del JsonOption
        return jsonify(dic)

    elif JsonOption['Gestion']=="DelCasoMon":
        ModelConsultas.FuncionUpdDelSpr(db,['SPR_DEL_CASO',JsonOption['CasoBuscar']])
        
        return ('', 204)
    elif JsonOption['Gestion']=="GetCasoMonAse":
        ArrayDatos = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1,
                                             "procedimiento": "SPR_GET_ESTCOMPASE",
                                             "arraydatos": [JsonOption['CasoBuscar']
                                                            ]})

        if JsonOption['Segmento'] != "HHPP":
            ItemsAfecCaso = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 2,
                                                    "procedimiento": "spr_get_itemafease",
                                                    "arraydatos": [JsonOption['CasoBuscar']
                                                                   ]})
        else:
            ItemsAfecCaso = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 2,
                                                    "procedimiento": "spr_get_itemafehp",
                                                    "arraydatos": [JsonOption['CasoBuscar']
                                                                   ]})
        if ArrayDatos != None:
            # ArrayDatos[-1]=str(ArrayDatos[1])#.strptime("%H:%H:%-S")
            dic = {"CompAse": ArrayDatos, "Notas": ItemsAfecCaso}
        else:
            dic = {"CompAse": 0, "Notas": ItemsAfecCaso}

        return json.dumps(dic, default=str)

    
    elif JsonOption['Gestion']=="UpdCompSup":
        ModelConsultas.FuncionUpdDelSpr(db,['SPR_UPD_MONCOMPSUP',[JsonOption['CasoBuscar'],JsonOption['CompSup']]])        
        return ('', 204)
        
    elif JsonOption['Gestion']=="UpdComAse":
        ModelConsultas.FuncionUpdDelSpr(db,['SPR_UPD_MONCOMPASE',[int(JsonOption['CasoBuscar']),JsonOption['CompAsesor']]])
        #flash("Compromiso creado con exito.")
        return ('', 204)
    elif JsonOption['Gestion']=="InsNueAse":
        try:
            Array=[]
            for i,j in enumerate(JsonOption['ArrayDatos']):
                if i==0:                    
                    Array.append(j)
                    Array.append(generate_password_hash(str(j)))
                else:
                    Array.append(j)        
            ModelConsultas.FuncionUpdDelSpr(db,['SPR_INS_NUEVOUSU',Array])
            res="Usuario creado con exito!"        
        except Exception as e:
            Nomb_error='Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e            
            res=str(e)
        dicResul={"Resultado":res}
        return json.dumps(dicResul, default=str)
    
    elif JsonOption['Gestion']=="UpdAse":
        ModelConsultas.FuncionUpdDelSpr(db,["spr_upd_aseexi",(JsonOption['ArrayDatos'])])
        return("",204)
                  
    elif JsonOption['Gestion']=="UpdCloseMuesta":
        SEL=ModelConsultas.FuncionGetSPR(db,["SPR_GET_COMPRS",JsonOption["CasoBuscar"]])
        for i in SEL:
            if i[0]==None and i[1]==None:
                return json.dumps({"Resultado":False,"CompFaltante":"Ambos"})
            elif i[0]!=None and i[1]==None:
                return json.dumps({"Resultado": False,"CompFaltante":"Asesor"})
            elif i[0]==None and i[1]!=None:
                return json.dumps({"Resultado": False,"CompFaltante":"Supervisor"})
            elif i[0] != None and i[1] != None:
                ModelConsultas.FuncionUpdDelSpr(db,['SPR_UPD_CLOMUESTRA',[JsonOption["Idusu"],JsonOption["CasoBuscar"]]])
                return json.dumps({"Resultado": True, "CompFaltante": False})
    
    elif JsonOption['Gestion']=="NuevaSol":
        IdSol=ModelConsultas.FuncionIns(db,["spr_ins_nuevsol",[JsonOption["Caso"],JsonOption["IdSol"],JsonOption["TipSol"],JsonOption["CauSol"],JsonOption["DesCas"]]])
        return json.dumps({"IdCaso": IdSol[0]})
    
    elif JsonOption['Gestion']=="DelSoli":
        ModelConsultas.FuncionUpdDelSpr(db,["spr_del_soli",[JsonOption["Caso"]]])
        return ('', 204)
    
    elif JsonOption['Gestion']=="ResponderSol":
        ModelConsultas.FuncionUpdDelSpr(db,["spr_ins_ressol",[JsonOption["Idsolicitud"],JsonOption["IdSolicitante"],JsonOption['ResSolicitud']]])
        return ('', 204)
    
    elif JsonOption['Gestion']=="GetEstadistica":
        if JsonOption["Perfil"]=="ASESOR":
            query = ModelConsultas.FuncionGetSPR(db, ['spr_get_stadistica', JsonOption['IdAsesor']])
            ArrayNotas=[]
            for i in range(len(query)):
                try:
                    ArrayNotas.append([float(Decimal(query[i][0])),float(100-Decimal(query[i][0]))])
                except:
                    ArrayNotas.append([0,0])
            return json.dumps({"ArrayNotasMesAct":ArrayNotas[0]})#,"ArrayNotasMesAnt":ArrayNotas[1],"ArrayNotasMesAnt2":ArrayNotas[2]})
        else:
            pass
        
    elif JsonOption['Gestion']=="Delcompase":
        ModelConsultas.FuncionUpdDelSpr(db,["spr_del_compase",[JsonOption["Caso"]]])
        return('', 204)

    # consultas para plantilla de notas
    elif JsonOption['Gestion'] == "InsdatNotas":
        DataForm = json.loads(JsonOption["DataNotas"])
        ConsultorApi().callUpd({'servicio': 'BotServer', 'ciudad': dicCiudad[JsonOption['Ciudad']], "tipo": 1, "procedimiento": "spr_ins_notdesp",
                                "arraydatos": [DataForm['OtLls'], DataForm['Id Usuario Cnd'],
                                json.dumps(JsonOption["DataNotas"]),JsonOption['Ciudad'], 'Registrado OK']})
        return json.dumps({"ResInsGes": 1})

    elif JsonOption['Gestion'] == "Gethisrazase":
        JsonDatos=[]
        if JsonOption['Asesor'] != None:
            JsonDatos = ConsultorApi().callGet(
                {'servicio': 'BotServer', 'ciudad': dicCiudad[current_user.ciudad], "tipo": 2, "procedimiento": "spr_get_hisrazase",
                 "arraydatos": [current_user.id]})
        return json.dumps(JsonDatos, default=str)

    elif JsonOption['Gestion'] == "Updreirazase":
        if 'IdRazon' in JsonOption and JsonOption['IdRazon'] is not None:
            ConsultorApi().callUpd({'servicio': 'BotServer', 'ciudad': dicCiudad[current_user.ciudad], "tipo": 2, "procedimiento": "spr_Upd_libotraz",
                                    "arraydatos": [JsonOption['IdRazon']]})
            return json.dumps({"Res": 1})
        else:
            return json.dumps({"Res": 0})


        # consultas para evaluaciones    
    elif JsonOption['Gestion']=="Insdateva":
        JsonProcess = HandleFiles(f"{app.static_folder}/ImgEvaluaciones", JsonOption['JsonEva']).makefolder()
        #ConsultorApi().callUpd({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1, "procedimiento": "spr_ins_dateva",
        # "arraydatos":[JsonOption['IdPret'],json.dumps(JsonOption['JsonEva']),JsonOption['Asesor']]})
        ConsultorApi().callUpd({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1, "procedimiento": "spr_ins_dateva",
                                "arraydatos": [JsonOption['IdPret'], json.dumps(JsonProcess), JsonOption['Asesor']]})
        #return json.dumps({"Res":1})
        # funciones para creador evaluaciones

        # returnar un archivo json
        directorio_destino = os.path.join(app.instance_path, 'UploadsPreturnos','JsonEvaluacion%s.json' % JsonOption['IdPret'])
        with open(directorio_destino, 'w') as archivo_json:
            json.dump(JsonOption['JsonEva'], archivo_json)

        return send_file(directorio_destino, as_attachment=True)

    elif JsonOption['Gestion']=="UpdEvaPreAse":
        Arraydatos = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1, "procedimiento": "spr_get_resbyeva","arraydatos":[JsonOption['IdEvaPre']]})                             
        Nota = CalNotaEva(Arraydatos,JsonOption['ArrayDatEva'])
        
        # ConsultorApi().callUpd({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1, "procedimiento":"spr_upd_resevapre","arraydatos":[JsonOption['Asesor'],JsonOption['IdEvaPre'],JsonOption['IdNumerario'],Nota,JsonOption['ArrayDatEva']]})
        ConsultorApi().callUpd({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1, "procedimiento": "spr_upd_resevapre",
                                "arraydatos": [JsonOption['IdEvaPre'],JsonOption['IdNumerario'],
                                               Nota, json.dumps(JsonOption['ArrayDatEva'])]})


        return json.dumps({"Nota":Nota})                      
        
    elif JsonOption['Gestion'] =="GetEstevabypre":
        Arraydatos=[]                
        if JsonOption['IdPreturno']:
            Arraydatos = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 2, "procedimiento": "spr_get_evaxpre","arraydatos":[JsonOption['IdPreturno']]})                             
        return json.dumps({"Evaluaciones":Arraydatos})
        
        
    
    elif JsonOption['Gestion'] == "GetNotasebypre":
        Arraydatos = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 2, "procedimiento": "spr_get_notasepre","arraydatos":[JsonOption['IdPreturno']]})                             
        
        return json.dumps({"AseEval":Arraydatos})

    elif JsonOption['Gestion'] =="GetNoteprebysup":
        Arraydatos = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 2, "procedimiento": "spr_get_notprebysup","arraydatos":[JsonOption['IdPreturno'],JsonOption['Idsuper']]})
        return json.dumps({"AseEval":Arraydatos})
    elif JsonOption['Gestion'] == "Getdatarazones":
        if current_user.perfil.lower == "supervisor":
            Arraydatos = ConsultorApi().callGet(
                {'servicio': 'BotServer', 'ciudad': dicCiudad[current_user.ciudad], "tipo": 2, "procedimiento": "spr_get_razbydia", "arraydatos":
                    [current_user.ciudad, current_user.campaña, current_user.id, JsonOption['DiaGestion']]})
        else:
            Arraydatos = ConsultorApi().callGet(
                {'servicio': 'BotServer', 'ciudad': dicCiudad[current_user.ciudad], "tipo": 2, "procedimiento": "spr_get_razbydia", "arraydatos":
                    [current_user.ciudad, current_user.campaña, current_user.nombre, JsonOption['DiaGestion']]})
        return json.dumps({"DataRazones": Arraydatos})

    elif JsonOption['Gestion'] == "Getdatraz":
        Arraydatos = ConsultorApi().callGet(
            {'servicio': 'BotServer', 'ciudad': dicCiudad[current_user.ciudad], "tipo": 1, "procedimiento": "spr_get_inforaz",
             "arraydatos": [JsonOption['idrazon']]})

        Arraydatos[5] = Trazador.mixhora(Arraydatos[5])
        Arraydatos[8] = Trazador.mixhora(Arraydatos[8])

        return json.dumps({"DataRazon": Arraydatos}, default=str)
    # ================================================ datos remociones ================================================
    elif JsonOption['Gestion'] == "InsNueRem":
        Radicado = ConsultorApi().FuncUpdGetSpr({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1,
                                                 "procedimiento": "spr_ins_nuremcal",
                                                 "arraydatos": [JsonOption['cedase'], JsonOption['Numerario'],
                                                                JsonOption['NotAse'], JsonOption['SegAsesor'],
                                                                json.dumps(JsonOption['ItemsAsesor'])
                                                     , JsonOption['ObsRemocion']]})

        return json.dumps({"Radicado": Radicado})

    elif JsonOption['Gestion'] == "Updestevausu":
        ConsultorApi().callUpd({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1,
                                "procedimiento": "spr_upd_resevausu",
                                "arraydatos": [JsonOption['IdEvaluacion']]})
        return json.dumps({"Res": 1})

    elif JsonOption['Gestion'] == "DelRem":
        ConsultorApi().callUpd({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1,
                                "procedimiento": "spr_del_remocion",
                                "arraydatos": [JsonOption['Numerario']]})
        return json.dumps({"Res": 1})


    elif JsonOption['Gestion'] == "SetMatRemocion":
        ConsultorApi().callUpd({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 2,
                                "procedimiento": "spr_upd_mattorem",
                                "arraydatos": [JsonOption['idremocion'], JsonOption['idmatrem'], current_user.id]})
        return json.dumps({"Res": 1})


    elif JsonOption['Gestion'] == "SetMonRemocion":
        ConsultorApi().callUpd({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 2,
                                "procedimiento": "spr_upd_monrem",
                                "arraydatos": [JsonOption['idremocion'], JsonOption['idmonrem'], current_user.id]})
        return json.dumps({"Res": 1})

    elif JsonOption['Gestion'] == "SetObsRemocion":
        ConsultorApi().callUpd({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 2,
                                "procedimiento": "spr_upd_obsrem",
                                "arraydatos": [JsonOption['idremocion'], current_user.id, JsonOption['obsergestion']]})
        return json.dumps({"Res": 1})

    # =============================================== ACTUALIZACION 26/04/2024 ==========================================
    elif JsonOption['Gestion'] == "SetTipiasesor":
        print(JsonOption['jsondatos'])
        ConsultorApi().callUpd({'servicio': 'BotServer', 'ciudad': dicCiudad[current_user.ciudad], "tipo": 2,
                                "procedimiento": "spr_upd_tipgesase",
                                "arraydatos": [JsonOption['jsondatos']['Contactabilidad'],
                                               JsonOption['jsondatos']['Gestion Realizada'],
                                               JsonOption['jsondatos']['Observaciones'],
                                               json.dumps(JsonOption['jsondatos']),
                                               JsonOption['jsondatos']['IdGestion']
                                               ]})
        return json.dumps({"Res": 1})  # ok

    elif JsonOption['Gestion'] == "Desbasbacks":

        ConsultorApi().callUpd({'servicio': 'BotServer', 'ciudad': dicCiudad[current_user.ciudad], "tipo": 1,
                                "procedimiento": "spr_upd_estbasback",
                                "arraydatos": [JsonOption['idbase'], current_user.id]})
        return json.dumps({"Res": 1})  # ok

    elif JsonOption['Gestion'] == "Updestbaseback":
        for idasesor, estadobase in JsonOption["JsonAsesores"].items():
            ConsultorApi().callUpd({'servicio': 'BotServer', 'ciudad': dicCiudad[current_user.ciudad], "tipo": 1,
                                    "procedimiento": "spr_upd_estgesbacklog",
                                    "arraydatos": [JsonOption['idbase'], JsonOption['EstadoBase'],
                                                   JsonOption['MotivoBase'],
                                                   idasesor, estadobase, current_user.id]
                                    })
        return json.dumps({"Res": 1})
    elif JsonOption['Gestion'] == "Updbasemongo":
        try:
            print("Actualizar informes")
            BotMongo=GestorConsultasshMongo()
            ResGes = threading.Thread(target=BotMongo.Main, args=(current_user.id, current_user.ciudad.capitalize(),),
                                         daemon=1).start()

            #ResGes = GestorConsultasshMongo().Main(current_user.id, current_user.ciudad.capitalize())
            print(ResGes)
            return json.dumps({"Res": ResGes})
        except Exception as e:
            print(2,e)
            return json.dumps({"Res": 0})
        # oveja
    else:
        return json.dumps({"AseEval": 1})

@app.route("/VistaCambioClave")
@login_required
def VistaCambioClave():
    return render_template('CambioPw.html')

@app.route("/UpdCredenciales",methods=['POST'])
@login_required
def UpdCredenciales():
    JsonOption = request.get_json()
    if JsonOption['Gestion']=="updpwaseext":
        ModelConsultas.FuncionUpdDelSpr(db, ['SPR_UPD_PW',[JsonOption['IdUsuario'], ModelUser.GenPass(JsonOption['NuePwUsu'])]])
        return ("",204)
    else:
        if ModelUser.CheckUpdPw(db,JsonOption['IdUsuario'],JsonOption['ClaveGetUsu']):
            ModelConsultas.FuncionUpdDelSpr(db,['SPR_UPD_PW',[JsonOption['IdUsuario'],ModelUser.GenPass(JsonOption['NuePwUsu'])]])
            return json.dumps({"ResCopClav":True})
        else:
            return json.dumps({"ResCopClav":False})

 ##modulo de informes
@app.route('/AdminUsuarios',methods=["GET","POST"])
@login_required
def AdminUsuarios():
    DicDatos=ModelUser.GetDataUsuario(db)
    return render_template("EleAdmin/GestionUsuarios.html",DicDatoUsu=DicDatos)
    

#manejo de errores navegacion
def estatus401(error):
    return redirect(url_for('login'))

def estatus404(error):
    return "<h1>Pagina no encontrada</h1>",404

@app.route('/download')
def download():
    pathdw = f"{RUTAlOCAL}/instance/Files/MonitorEventos.exe"
    return send_file(pathdw, as_attachment=True)

@app.route('/dwexe/<appname>')
def dwexe(appname):
    if appname=="Monitor Koala":
        pathdw = f"{RUTAlOCAL}/instance/Files/VisorEventos.exe"
    elif appname=="Orquestador CND" or appname=="orquestador":
        pathdw = f"{RUTAlOCAL}/instance/Files/OrquestadorBotsCND.exe"
    elif appname=="Monitor calidad":
        pathdw = f"{RUTAlOCAL}/instance/Files/MonitorCalidad.exe"
    elif appname=="Facturador RR":
        pathdw = f"{RUTAlOCAL}/instance/Files/BotUtpAs400.exe"
    elif appname=="MonitorEventos":
        pathdw = f"{RUTAlOCAL}/instance/Files/MonitorEventos.exe"
    elif appname== "Cancelador RR" or appname=="RRCancelacionRazones":
        pathdw = f"{RUTAlOCAL}/instance/Files/RRCancelacionRazones.exe"
    elif appname== "Utp RR":
        pathdw = f"{RUTAlOCAL}/instance/Files/BotUtpAs400.exe"
    elif appname== "Bot hhpp":
        pathdw = f"{RUTAlOCAL}/instance/Files/LanzadorBotHHPP.exe"

    return send_file(pathdw, as_attachment=True)

##modulo de informes
@app.route('/VistaInformes',methods=["GET","POST"])
@login_required
def VistaInformes():
    return render_template("Eleinformes/vistaInformes.html")

## modulo de chats modulo experimental
# se debe conccer id de asesor



@app.route('/downloadCsv',methods=["GET","POST"])
def downloadFile(csvFileName): #In your case fname is your filename
    try:
        path = f"{RUTAlOCAL}/instance/downloads/{csvFileName}"
        return send_file(path, mimetype='text/csv', attachment_filename=csvFileName, as_attachment=True)
    
    except Exception as e:
        return str(e)
    
    
@app.route('/dwInformes',methods=["GET","POST"])
def dwInformes():
    if request.form['seltipInfo']=="..Seleccione...":
        return("",204)
    else:
        query=ModelConsultas.FuncionGetSprInf(db,["spr_get_infogral",[request.form['inpfecIniInf'],request.form['inpfecFinInf']]])
        pathDw = f"{RUTAlOCAL}/instance/downloads/InformeGeneralCalidad.xls"
        ArrayEncabezados=["IdMuestra", "Cedula  Asesor", "Nombre asesor", "Campaña", "Supervisor", "Login", "Fecha ingreso",
         "Antigüedad", "Razon", "Cuenta", "Orden",
         "fecha monitoreo", "fecha gestion", "Auditor", "Nota monitoreo", "tipo trabajo","Ciudad","Estado Monitoreo","Observaciones",
        "CompAgente","FechaComAgente","CompSupervisor","FecComSupervisor","ItemsCumple","ItemsNoCumple"]


        ArrayTemp=[]
        for i in query:
            IdMon=i[0]
            NotasItems=ModelConsultas.GestorItems(db,IdMon)
            i+=NotasItems
            ArrayTemp.append(i)
        MakeInf(ArrayEncabezados,ArrayTemp,pathDw)
        return send_file(pathDw, as_attachment=True)
        
        
        
@app.route('/GetDatoUser',methods=["POST"])
def GetDatoUser():
    JsonOption = request.get_json()    
    Option= JsonOption['Gestion']    
    if Option=="getdatasecon":
        data=ModelConsultas.FuncionGetSPR(db,["spr_get_infoasexced",JsonOption['cedase']])
        if len(data)>0:
            return json.dumps({"DicDatos":data[0]},default=str)
        else:
            return json.dumps({"DicDatos":[]},default=str)
    
    return ("",204)
    
    
@app.route("/FormateaClave")
@login_required
def FormateaClave():
    return render_template("/EleAdmin/vistaClaves.html")
    

@app.route("/AdminItemCalidad")
@login_required
def AdminItemCalidad():
    return render_template("/EleCalidad/VistaItemsCal.html")
    
#MODULOS PARA FORMACION
#ENRRUTADORES A PAGINAS Y VISTAS
@app.route("/Enrrutador/<application_name>", methods=['GET', 'POST'])
@login_required
def Enrrutador(application_name):
    if application_name=="ConsultaPreturno":
        return render_template("/EleFormacion/vistapreturnos.html")

    elif application_name=="CrearEvaluacion":
        return render_template("/EleFormacion/CreadorEvaluacion.html")

    elif application_name=="SubirPreturno":
        return render_template("/EleFormacion/NuevoPreturno.html")

    elif application_name=="VerPreturno":
        return render_template("/EleFormacion/ConsultarPreturno.html")

    elif application_name=="NotasEvaluacion":
        return render_template("/EleFormacion/NotasEvaluacion.html")

    elif application_name=="CargarFilesGerencia":
        return render_template("/EleGerencia/GestorFiles.html")

    elif application_name=="EnDesarrollo":
        return render_template("/Endesarrollo.html")

    elif application_name == "HistorialRazones":
        return render_template("/EleGestion/HistorialRazones.html")
    #================Remociones================
    elif application_name == "RegistrarRemocion":
        return render_template("/Remociones/RegistrarRemocion.html")

    elif application_name == "HistorialRemocion":
        if current_user.is_authenticated:
            data = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 2,
                                           "procedimiento": "spr_gethisremo",
                                           "arraydatos": [current_user.cargo, current_user.nombre,current_user.ciudad]})
        else:
            return redirect(url_for('login'))
        return render_template("/Remociones/HistorialRemociones.html", ArrayRemociones=data)

    # #====================== modificacion 23/04/04 para incluri labor backlog=====================
    elif application_name=="PlaBacklog":
        DicConfvista={"Gestiones":["Enviar a completar","Enviar a cancelar"],"codCierre":["LSC","N04"]}
        return render_template("/EleGestion/PlantillaBack.html",DicConfvista=DicConfvista)
    elif application_name=="Asignacionback":
        #dicdatos= ConsultorApi().callGet({'servicio': 'BotServer', 'ciudad': 1, "tipo": 1,
        #                                "procedimiento": "spr_get_paterrazon","arraydatos":[]})
        return render_template("/EleGestion/Asigbasesback.html")#,data=dicdatos)
    else:
        return render_template("/home2.html")


        


@app.route("/uploader", methods=["GET","POST"])
@login_required
def uploader():    
    if request.method == 'POST':
        Opcion=request.form["OpcionGestion"]
        IdFile=request.form["IdFile"]
        file = request.files['filepdfpreturno']
        Nombrepreturno=request.form["inpnompreturno"]
        fechapreturno=request.form["inpfecingpreturno"]
        descpretunro=request.form["inpdespreturno"]
        SegmentoPreturno = request.form["SelSegmento"]
        TipoPreturno = request.form["Seltipoges"]
        linkeva="http://172.20.100.51:443/Endesarrollo.html"
        #linkeva=request.form['inpevapreturno']
        usucargue = request.form['inpusucargue']
        ciucargue = request.form['inpciucar']
        if file.filename!="":
            filename = secure_filename(file.filename)
            try:
                file.save(os.path.join(app.instance_path, 'UploadsPreturnos', filename))
            except Exception as e:
                print("Error al guardar el archivo:", e)

            path = f"{RUTAlOCAL}/instance/UploadsPreturnos/{filename}"

        if Opcion=="Nuevo":
            ModelConsultas.FuncionIns(db,["spr_ins_upfile",[Nombrepreturno,fechapreturno,0,descpretunro,"Formacion",TipoPreturno,path,linkeva,usucargue,ciucargue,SegmentoPreturno]])
        else:
            ModelConsultas.FuncionIns(db,["spr_upd_detfile",[IdFile,Nombrepreturno,fechapreturno,0,descpretunro,"Formacion",TipoPreturno,path,linkeva,SegmentoPreturno]])

        flash("Preturno cargado con exito!!!")
        return redirect(url_for("Enrrutador",application_name="SubirPreturno"))


@app.route("/uploaderFilGer", methods=["GET", "POST"])
@login_required
def uploaderFilGer():
    if request.method == 'POST':
        Opcion = "Nuevo"
        idusuario = current_user.id
        # IdFile = request.form["IdFile"]
        file = request.files['formFileSm']
        TipoFile = request.form["inpTipoFile"]
        RegionalFile = request.form["inpRegionfile"]
        descFile = request.form["inpdesfile"]

        if file.filename != "":
            file.filename = secure_filename(file.filename)
            path0 = os.path.join(RUTAlOCAL, 'instance\RepositorioClaro')
            path1 = CreadorCarpetas(path0)
            RutaSAVE = f"{path1}\{TipoFile}_{RegionalFile}_{file.filename}"
            #print(RutaSAVE)
            if os.path.isfile(RutaSAVE) == False:
                file.save(RutaSAVE)
                # ModelConsultas.FuncionIns(db,["spr_ins_upfile",[Nombrepreturno,fechapreturno,0,descpretunro,"Formacion",TipoPreturno,path,linkeva,usucargue,ciucargue,SegmentoPreturno]])
                ModelConsultas.FuncionIns(db, ["spr_ins_upfile",
                                               [f"{TipoFile}_{RegionalFile}_{file.filename}", "N/A", 0, descFile,
                                                "Gerencia", "Archivo de respaldo",
                                                RutaSAVE, "N/A", idusuario, current_user.ciudad, "N/A"]])
                ResultadoCarga = "Archivo cargado con exito"
            else:
                ResultadoCarga = "Ya existe un archivo con el mismo nombre, Favor cambie el nombre de su archivo"

        flash(ResultadoCarga)
        return redirect(url_for("Enrrutador", application_name="CargarFilesGerencia"))

@app.route("/ConsultorDatos", methods=["GET","POST"])
@login_required
def ConsultorDatos():
    JsonOption = request.get_json()

    if JsonOption['Option'] =="GetPreturnosActivos":
        data=ModelConsultas.FuncionGetSPR(db,["spr_get_filform"])
        return json.dumps(data)
    
    elif JsonOption['Option']=='DelPretFile':        
        ModelConsultas.FuncionUpdDelSpr(db,["spr_del_file",JsonOption['PretId']])
        return redirect(url_for("Enrrutador",application_name="SubirPreturno"))
    
    elif JsonOption['Option']=='DwPretFile':
        path = ModelConsultas.FuncionGetSprInf(db,["spr_get_xpathfile",JsonOption['PretId']])
        FileName=path[0][0]
        path=path[0][1]

        return send_file(path_or_file=path,mimetype='application/pdf',download_name=f"{FileName}.pdf" ,as_attachment=True)

    elif JsonOption['Option']=='DwFile':
        path = ModelConsultas.FuncionGetSprInf(db,["spr_get_xpathfile",JsonOption['PretId']])                
        FileName=os.path.split(path[0][1])[1]
        return send_file(path_or_file=path[0][1],mimetype='application/*',download_name=FileName ,as_attachment=True)
    
    elif JsonOption['Option']=='GetFilemes':
        if JsonOption['mesdata']=='Todos':
            data = ModelConsultas.FuncionGetSPR(db, ["spr_get_filgere"])
        else:
            data = ModelConsultas.FuncionGetSPR(db, ["spr_get_filgeremes", dicMes[JsonOption['mesdata']]])
        return json.dumps(data)
    
    elif JsonOption['Option']=='Getpretmes':
        data = ModelConsultas.FuncGetSpr(db, 2, "spr_get_filformmes",
                                         [JsonOption['mesdata'], JsonOption['yeardata'], current_user.ciudad,
                                          current_user.id])
        return json.dumps(data,default=str)

    elif JsonOption['Option'] == 'GetpretmesAsesor':
        Segmento = "MASIVO" if current_user.perfil != "HHPP" else "HHPP"
        data = ModelConsultas.FuncGetSpr(db, 2, "spr_get_premesasesor",
                                         [JsonOption['mesdata'], JsonOption['yeardata'], current_user.ciudad,
                                          current_user.id, Segmento]
                                         )
        return json.dumps(data, default=str)

    elif JsonOption['Option']=='Getevabypre':
        if JsonOption['mesdata']=='Todos':
            data = ModelConsultas.FuncGetSpr(db,2,"spr_get_evabypre",[JsonOption['CiuData']])
        else:
            data = ModelConsultas.FuncGetSpr(db,2,"spr_get_evabypremes",[JsonOption['mesdata'],JsonOption['CiuData']])
        return json.dumps(data,default=str)

    elif JsonOption['Option']=='GetNotpretmesAse':        
        data= ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 2,
                    "procedimiento": "spr_get_notprease","arraydatos":[dicMes[JsonOption['mesdata']]]})                         
        return json.dumps(data)
    
    elif JsonOption['Option']=="GetDetaPretu":
        data = list(ModelConsultas.FuncionGetSPR(db, ["spr_get_detfile",JsonOption['PretId']]))        
        return json.dumps({"ArrayData":data},default=str)
   
    elif JsonOption['Option']=="Getcambyciudad":
        data = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 2, "procedimiento": "spr_get_supbyciud","arraydatos":[JsonOption['Ciudad']]})                                     
        return json.dumps({"ArrayData":data},default=str)
    
    elif JsonOption['Option']=="Getasebycamp":        
        data = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 2, "procedimiento": "spr_get_asiprease","arraydatos":[JsonOption['idpreturno'],JsonOption['IdCiudad'],JsonOption['Segmento'] ]})
        return json.dumps({"ArrayData":data},default=str)        
    
    elif JsonOption['Option']=="InsAsiPreturnos":
        # traer los datos de la base de datos idpreturno para comparar
        matrix0 = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 2,
                                          "procedimiento": "spr_upd_asibypret",
                                          "arraydatos": [JsonOption['idpreturno']]})

        matrix1 = JsonOption['arraydatos']
        if matrix0 != None:
            dict_matrix0 = {row[0]: row for row in matrix0}
            # se ben guardar datos nuevos y de las personas que tenadn check de gestion
            for dato in matrix1:
                cedAsesor = int(dato[2])
                boolasis = int(dato[3])
                boolnov = int(dato[4])

                if cedAsesor in dict_matrix0:
                    # busca i en la matrix 0 y comarara con lo que viene de front
                    dbasistencia = int(dict_matrix0[cedAsesor][3])
                    dbnovedad = int(dict_matrix0[cedAsesor][6])

                    if dbasistencia != boolasis or boolnov != dbnovedad:

                        ConsultorApi().callUpd(
                            {'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1, "procedimiento": "spr_upd_estasipre",
                             "arraydatos": dato})
                    else:
                        pass
                else:
                    ConsultorApi().callUpd(
                        {'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1, "procedimiento": "spr_ins_asipre",
                         "arraydatos": dato})
        else:
            for dato in matrix1:
                if int(dato[3]) != 0 or int(dato[4]) != 0:
                    # guardar los datos que si apliquen check
                    ConsultorApi().callUpd(
                        {'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1, "procedimiento": "spr_ins_asipre",
                         "arraydatos": dato})
        return ("", 204)

        for datos in JsonOption['arraydatos']:            
            data = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1, "procedimiento": "spr_get_estasipre","arraydatos":[datos[0],datos[2]]})                                                                                 
            if data!=None:
                ConsultorApi().callUpd({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1, "procedimiento": "spr_upd_estasipre","arraydatos":datos})                                                                 
            else:
                ConsultorApi().callUpd({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1, "procedimiento": "spr_ins_asipre","arraydatos":datos})                                                                 
        return ("",204)
    
    elif JsonOption['Option']=="Getclase":
        ArrayCred=ModelConsultas.FuncGetSpr(db,1,"spr_get_claase", [JsonOption['CodAse']])        
        
        if ArrayCred==None:
            ArrayCred={}
            return json.dumps({'DicDatcla':{}}, default=str)   
        else:
            dicCred={}            
            dicCred['UsuarioModulo']=GestorEnccycode.decripcode(ArrayCred[0])
            dicCred['ClaveModulo']=GestorEnccycode.decripcode(ArrayCred[1])
            dicCred['FechModulo']=ArrayCred[2]
            dicCred['UsuarioWMF']=GestorEnccycode.decripcode(ArrayCred[3])
            dicCred['ClaveWMF']=GestorEnccycode.decripcode(ArrayCred[4])
            dicCred['FechWFM']=ArrayCred[5]
            dicCred['UsuarioAS400']=GestorEnccycode.decripcode(ArrayCred[6])
            dicCred['ClaveAS400']=GestorEnccycode.decripcode(ArrayCred[7])
            dicCred['FechAS400']=ArrayCred[8]                        
            return json.dumps({'DicDatcla':dicCred}, default=str)   
      
    elif JsonOption['Option']=="updpwase": 
        usuario=GestorEnccycode.encripcode(JsonOption['Usser'])
        clave=GestorEnccycode.encripcode(JsonOption['pws'])         
        ModelConsultas.FuncionUpdDelSpr(db,["spr_upd_credase",[JsonOption['Usuario'],JsonOption['apk'],usuario,clave,JsonOption['sup']]])
        
        return json.dumps({'DicDatupd':"Envio base de datos ok"}, default=str)
    elif JsonOption['Option'] == "getdatasecon":
        data = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1,
                                       "procedimiento": "spr_get_infoasexced", "arraydatos": [JsonOption['cedase']]})
        if data != None:
            return json.dumps({"DicDatos": data}, default=str)
        else:
            return json.dumps({"DicDatos": []}, default=str)

    elif JsonOption['Option'] == "getitemsbyseg":
        data = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 2,
                                       "procedimiento": "spr_get_itemsbyseg", "arraydatos": [JsonOption['Campaña']]})

        return json.dumps({"DicDatos": data}, default=str)

    elif JsonOption['Option'] == "GetdatRem":
        # informacion remocion
        DataAsesor = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1,
                                             "procedimiento": "spr_getdataserem",
                                             "arraydatos": [JsonOption['Numerario']]})

        # informacion formacion
        # if ya esta escogido trae las notas de la evaluacion asociada a ese preturno
        DicBotones = {"btnasimatest": 0, "btndwpret": 0, "btnevaluacion": 0, "btnasimonrem": 0, "btnguacomsuprem": 0}
        if DataAsesor[11] == None:
            # 1  trae los preturnos del mes
            DataMaterial = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 2,
                                                   "procedimiento": "spr_get_remmes",
                                                   "arraydatos": [datetime.datetime.now().month, current_user.ciudad]})
            DicBotones['btnasimatest'] = 1
        else:
            DataMaterial = []
            DicBotones["btndwpret"] = 1
            DicBotones["btnevaluacion"] = 1
        # informacion calidad
        # trae los monitoreos asociado al asesor del mes
        # si ya esta escogido, trae las notas del monitoreo
        # si ya esta escogido, trae las notas del monitoreo
        if DataAsesor[21] == None:
            DataMonAsesor = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 2,
                                                    "procedimiento": "spr_get_cmonxase",
                                                    "arraydatos": [DataAsesor[0]]})

            DicBotones['btnasimonrem'] = 1
        else:
            DataMonAsesor = []

        DicBotones["btnguacomsuprem"] = 1 if DataAsesor[29] == None else 0
        return json.dumps({"DataAsesor": DataAsesor, "DataMaterial": DataMaterial, "DataMonAsesor": DataMonAsesor,
                           "DicBotones": DicBotones})

    elif JsonOption['Option'] == "getimgrazon":
        #if current_user.ciudad.lower() != "bogota":
        if current_user.ciudad.lower() == "cali":
            url = "http://10.206.170.19:3541/Getimagen?procedimiento=%s&idevento=%s"%("spr_get_paterrazon", JsonOption['Evento'])
        else:
            url = "http://192.150.100.7:3541/Getimagen?procedimiento=%s&idevento=%s" % (
            "spr_get_paterrazon", JsonOption['Evento'])

        response = requests.get(url)
        imggestion = os.path.join(PATHINSTANCE, 'Tempservcali', f'ImgGestion_{JsonOption["Evento"]}.png')
        with open(imggestion, 'wb') as f:
            f.write(response.content)
        return send_file(imggestion, mimetype='image/png', download_name=f'ImgGestion_{JsonOption["Evento"]}.png',
                         as_attachment=True)

        '''else:
            pathdw = ConsultorApi().callGet({'servicio': 'BotServer', 'ciudad': 1, "tipo": 1,
                                             "procedimiento": "spr_get_paterrazon", "arraydatos": [JsonOption['Evento']]})
            if pathdw[0] != None:
                nombre_archivo = os.path.split(pathdw[0])
                return send_file(os.path.normpath(pathdw[0]), mimetype='image/png', download_name=nombre_archivo[1], as_attachment=True)
            else:
                return send_file(app.static_folder + "\img\confusedBot.png", mimetype='image/png',
                                 download_name="NoFoudImg.png", as_attachment=True)'''
    elif JsonOption['Option'] == "getcomresase":
        ArrayDatos = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 1,
                                             "procedimiento": "spr_get_resevaase",
                                             "arraydatos": [JsonOption['IdEvaluacion']]})

        if ArrayDatos != None:
            pathdw = f"{RUTAlOCAL}/instance/Uploads/FileRespAsesor.csv"
            createcsvrespuestas(ArrayDatos, pathdw)
            return send_file(pathdw, mimetype='text/csv',
                             download_name=f"RespEvaluacion-{JsonOption['IdEvaluacion']}.csv", as_attachment=True)
        else:
            return ("", 204)

    elif JsonOption['Option'] == "GetNotEvaPre":
        ArrayDatos = ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': dicCiudad[current_user.ciudad], "tipo": 2,
                                             "procedimiento": "spr_get_notbypre",
                                             "arraydatos": [JsonOption['IdPreturno']]})

        if ArrayDatos != None:
            pathdw = f"{RUTAlOCAL}/instance/Uploads/FileRespPreturno.csv"
            InformesMasivo(ArrayDatos).Main(pathdw)
            return send_file(pathdw, mimetype='text/csv', download_name=f"RespPreturno-{JsonOption['IdPreturno']}.csv",
                             as_attachment=True)
        else:
            return ("", 204)
    ## =============================actualizacion 22/04/2024 para consultar ordees canceladas desde crm =============================
    elif JsonOption['Option'] == "Gethiscanase":
        ArrayDatos = ConsultorApi().callGet({'servicio': 'BotServer', 'ciudad': dicCiudad[current_user.ciudad], "tipo": 2,
                                             "procedimiento": "spr_get_hiscanase", "arraydatos": [current_user.id]})
        return json.dumps({"Arraydatos": ArrayDatos})

    ## ============================deben ir a bot server por la idea de la gestion de los bots de as400 ============================

    elif JsonOption['Option'] == "Gethisgesback":
        ArrayDatos = ConsultorApi().callGet({'servicio': 'BotServer', 'ciudad': dicCiudad[current_user.ciudad], "tipo": 2,
                                             "procedimiento": "spr_get_hisbasback",
                                             "arraydatos": [JsonOption['Fecha'],current_user.ciudad]})
        return json.dumps({"Arraydatos": ArrayDatos}) #ok

    elif JsonOption['Option'] == "Getgesback":
        ArrayDatos = ConsultorApi().FuncUpdGetSpr({'servicio': 'BotServer', 'ciudad': dicCiudad[current_user.ciudad],
                                                   "tipo": 1,
                                                   "procedimiento": "spr_get_otsgesback",
                                                  "arraydatos": [current_user.id]})

        arraydata = []
        arrayrazones = []

        '''if ArrayDatos!=None:
            arraydata = Handledbmongo(nombreDb='db_hinformes_cnd').GetData("ActividadesWfmnacional",
                                                                              {"Orden de trabajo Mantenimientos 7K":
                                                                                   {"$regex": ArrayDatos[3],
                                                                                    "$options": "i"}},
                                                                               {'_id': 0,'CAMBIOEQ_GESTION':1})

            time.sleep(1)
            arraydatadia = Handledbmongo(nombreDb='db_hinformes_cnd').GetData(
                diccolavancebyciudad[current_user.ciudad.capitalize()],
                {"Orden de trabajo Mantenimientos 7K":
                     {"$regex": str(ArrayDatos[3]), "$options": "i"}},
                {'_id': 0, 'CAMBIOEQ_GESTION': 1})

            time.sleep(1)
            Arraycnt = ConsultorApi().callGet({'servicio': 'BotServer', 'ciudad': dicCiudad[current_user.ciudad], "tipo": 1,
                                               "procedimiento": "spr_get_cntgesback", "arraydatos": [ArrayDatos[3]]})
            if Arraycnt!=None:
                ArrayDatos.append(Arraycnt[0])
            else:
                ArrayDatos.append(0)

            if len(arraydatadia) != 0:
                for i in arraydatadia:
                    arrayrazones.append(replace_nan_with_none(i['CAMBIOEQ_GESTION']))

            if len(arraydata) != 0:
                for i in arraydata:
                    arrayrazones.append(replace_nan_with_none(i['CAMBIOEQ_GESTION']))'''

        return json.dumps({"Arraydatos": ArrayDatos,"DetalleRazon":arrayrazones})  # ok

    elif JsonOption['Option'] == "Getotsfuturas":
        ArrayDatos = ConsultorApi().callGet({'servicio': 'BotServer', 'ciudad': dicCiudad[current_user.ciudad], "tipo": 2,
                                             "procedimiento": "spr_get5otsback", "arraydatos": [current_user.id]})

        return json.dumps({"Arraydatos": ArrayDatos})  # ok

    elif JsonOption['Option'] == "Getbasupdback":
        ArrayDatos = ConsultorApi().callGet({'servicio': 'BotServer', 'ciudad': dicCiudad[current_user.ciudad], "tipo": 2,
                                             "procedimiento": "spr_get_basactback","arraydatos":[current_user.ciudad]})

        #spr_get_basupdback
        return json.dumps({"Arraydatos": ArrayDatos})  # ok

    elif JsonOption['Option'] == "Getdwgesback":
        ArrayDatos = ConsultorApi().callGet(
            {'servicio': 'BotServer', 'ciudad': dicCiudad[current_user.ciudad], "tipo": 2,
             "procedimiento": "spr_get_dwgesback", "arraydatos": [JsonOption['Fecha'], current_user.ciudad]})

        foldersecuresave = CreadorCarpetas(os.path.join(PATHINSTANCE, 'Tempdownloads'))
        pathfile = os.path.join(foldersecuresave, "GestionBacklog.csv")
        ArrayEncabezados = ["IdGestion", "Tiporden", "Cuenta", "Otlls", "Edad", "Estadovisita", "Razon",
                            "EstadoRegistro", "Fecharegistro",
                            "Horaregistro", "Asignado", "Idasesor", "Fechaasignacion", "Horaasignacion",
                            "Gestionasesor", "Fechagesasesor", "Horgesasesor",
                            "Contato", "Gestioncontacto", "Obsergestion", "Jdatages", "Estgesas400", "Fechagesas400",
                            "Horgesas400", "Obsgesas400"]
        tinformes = threading.Thread(target=generarInformeCsv, args=(pathfile, ArrayEncabezados, ArrayDatos,), daemon=1)
        tinformes.start()
        tinformes.join()
        # return send_file(pathdw[0], mimetype='image/png', download_name=nombre_archivo[1],as_attachment=True)
        return send_file(pathfile, mimetype='text/csv', download_name="GestionBacklog.csv", as_attachment=False)

    elif JsonOption['Option'] ==  "Getmetrisback":
        ArrayDatos = ConsultorApi().callGet({'servicio': 'BotServer', 'ciudad': dicCiudad[current_user.ciudad], "tipo": 2,
                                        "procedimiento": "spr_get_metusuback","arraydatos":[JsonOption['Fecha'],current_user.ciudad]})
        return json.dumps({"Arraydatos":ArrayDatos})

    # ==========================ACTUALIZACION 14-05-2024 PARA CONSULTAS BASES BACKLOG SUPERVISOR ====================
    elif JsonOption['Option'] == "Getbasebackdia":
        ArrayDatos = ConsultorApi().callGet(
            {'servicio': 'BotServer', 'ciudad': dicCiudad[current_user.ciudad], "tipo": 2,
             "procedimiento": "spr_get_basbydia", "arraydatos": [JsonOption['Fecha'], current_user.ciudad]})

        return json.dumps({"Arraydatos": ArrayDatos})

    elif JsonOption['Option'] == "Getmetbybase":
        ArrayDatos = ConsultorApi().callGet(
            {'servicio': 'BotServer', 'ciudad': dicCiudad[current_user.ciudad], "tipo": 2,
             "procedimiento": "spr_get_metbybase", "arraydatos": [JsonOption['IdBase']]})

        return json.dumps({"Arraydatos": ArrayDatos})
    else:
        print(JsonOption['Option'])


@app.route("/GetdataAPI", methods=["GET", "POST"])
@login_required
def GetdataAPI():
    JsonFront = request.get_json()
    ### Subir este dicionario a mongo
    dicGeneral = {"Getdetgesord": {"NFilas": 1, "Proc": "spr_get_detgeotsback", "param": [JsonFront['norden']]}
                  }
    dicrel = dicGeneral[JsonFront['Req']]
    ArrayDatos = ConsultorApi().callGet({"servicio": "BotServer", "ciudad": dicCiudad[current_user.ciudad], "tipo": dicrel["NFilas"],
                                         "procedimiento": dicrel["Proc"], "arraydatos": dicrel['param']})

    return json.dumps({"Arraydatos": ArrayDatos})  # ok
    JsonOption = request.get_json()


@app.route('/Sendbasebacklog', methods=['POST'])
def Sendbasebacklog():
    file = request.files['inpfilbasbacklog']
    nameFile = secure_filename(file.filename)
    foldersecuresave = CreadorCarpetas(os.path.join(PATHINSTANCE, 'UploadBacklog'))
    PathFile = os.path.join(foldersecuresave, nameFile)
    file.save(PathFile)
    ## leer el archivo y enviar los datos al la base de datos
    ## al tener las bases de datos separadas se debe hacer una consulta para traer el nombre del asesor
    dataAsesor= ConsultorApi().callGet({'servicio': 'CrmCalidad', 'ciudad': 1, "tipo": 2,
                    "procedimiento": "spr_get_nomasebyciu","arraydatos":[current_user.ciudad]})
    # =================================================================================================

    ArrayDatos = Lector.lectorcsv(PathFile)
    botconn = ConectorDbMysql(current_user.ciudad)
    subproceso = threading.Thread(target=botconn.upload,
                                  args=(current_user.id, "spr_ins_basbackog", PathFile, ArrayDatos,dataAsesor))
    subproceso.start()
    return redirect(url_for("Enrrutador", application_name="Asignacionback"))

        
if __name__=='__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401,estatus401)
    app.register_error_handler(404, estatus404)
    
    serve(app, host="0.0.0.0", port=443,threads=200,url_scheme='https',connection_limit=200, backlog=2048)
    #serve(app, host="0.0.0.0", port=443, threads=200, connection_limit=200, backlog=2048)
    #app.run(host="0.0.0.0",port=5000)
    #socketio.run(app=app,host="0.0.0.0", port=443)
