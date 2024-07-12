

from os import curdir
from telnetlib import PRAGMA_HEARTBEAT
from traceback import print_tb
from flask import Flask,render_template,request,redirect,url_for,flash,jsonify
from flask_mysqldb import MySQL

from config import config
from flask_login import LoginManager,login_user,logout_user,login_required
from flask_wtf.csrf import CSRFProtect

#modelos
from models.ModelUser import ModelUser
from models.entities.User import User

from models.ModelBots import ModelBots
from models.entities.Bots import Bot

from models.ModeloItemsMon import ModelConsultas

from models.Matematico import  CalNotaMon, ExtDataDic

import json

app=Flask(__name__)

csrf = CSRFProtect()



db=MySQL(app)



login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.Get_by_id(db,id)


"""
Enable CORS. Disable it if you don't need CORS
https://parzibyte.me/blog
"""
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

        else:
            flash("Usuario no encontrado...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/DashboardCND')
def DashboardCND():
    
    return render_template('home2.html')


#background process happening without any refreshing
@app.route('/GetDataAseMOn',methods=['POST'])
@login_required
def GetDataAseMOn():
    user = request.form.get('ced')
    data=ModelUser.getDatAseMon(db,user)
    if data==None:
        data=[None,None,None,None,None,None]
    else:
        pass
    return jsonify({'Nombre' : data[0],'Proceso':data[1],'Estado':data[2],'cordinador':data[3],
                    'fechIngreso':data[4],'formador':data[5]})

#Consulta los datos del formulario
@app.route('/GetDataFormMon',methods=['POST'])
@login_required
def GetDataFormMon():
    Camp = request.form.get('Campaña')
    data=ModelConsultas.GetDataFormMon(db,Camp)

    if data==None:
        data=[None,None,None,None,None,None]
    else:
        pass

    x=jsonify({'DicDatForm': data})
    return x

@app.route('/CalcNotaMon',methods=['POST'])
@login_required
def CalcNotaMon():
    DicDatosFor = request.form.get('DatoForm')
    res = json.loads(DicDatosFor)
    ArrayNotas=CalNotaMon(res)
    return jsonify({'TotalCrit':int(ArrayNotas[0]),'TotalNoCritico':int(ArrayNotas[1]),'SumaCritico':int(ArrayNotas[2]),'NotaTotal' : int(ArrayNotas[3]),'ItemsAfec':ArrayNotas[4]})

@app.route('/updgestionMon', methods=['POST'])
@login_required
def updgestionMon():
    ArrayDatosForMon = request.form.get('DatoMon')
    res = json.loads(ArrayDatosForMon)
    NumeroRad=ModelConsultas.InsDataForm(db,ExtDataDic(res))
    del res, ArrayDatosForMon
    return jsonify({"RadMonitoreo":NumeroRad})





## funciones complementarias ##
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


#rutas protegidas
@app.route('/NuevoMonitoreo')
@login_required
def NuevoMonitoreo():
    contador=0
    ArrayRangos=[]
    for i in range(6,22):
        for j in range(2):
            if j==0:
               ArrayRangos.append(f"{str(i).zfill(2)}:{str(contador).zfill(2)} a {str(i).zfill(2)}:{contador+30}")
            elif j==1:
                ArrayRangos.append(f"{str(i).zfill(2)}:{str(int(contador+30)).zfill(2)} a {str(int(i+1)).zfill(2)}:{str(contador).zfill(2)}")

    DicDatos={
        "CUENTA":"CLARO CND BOGOTA",
        "CIUDAD":["BOGOTA","CALI"],
        "AREAMON":["CALIDAD","MEC","SUPERVISOR","FORMACION"],
        "AUDITOR":[
            {"NombreAud":"JOAN CAMILO SERRANO CHAVEZ","CedAud":1022955073},
            {"NombreAud":"MILTON GIOVANNI TIRIA CORREDOR","CedAud":1012370702},
            {"NombreAud":"SONIA LISBETH SAAVEDRA RAMIREZ","CedAud":1015430024},
            {"NombreAud":"MANUEL FABIAN USECHE HENAO","CedAud":1026290405},
            {"NombreAud":"MEC","CedAud":"MEC"},
            {"NombreAud":"JEFFREY ARLEX GARCIA ARARTH","CedAud":1144025554},
            {"NombreAud":"SANDRA ASTRID FERNANDEZ GAMEZ","CedAud":1013605963},
            {"NombreAud":"LUZ ADRIANA RESTREPO ROA","CedAud":52846414},
            {"NombreAud":"WESLEY CHAPARRO SANABRIA","CedAud":1014238085},
            {"NombreAud":"SANTIAGO ALEJANDRO GARCIA MARTINEZ","CedAud":1022411312}
            ],
        "TIPOAUD":["MUESTRA","REMOTO","LADO A LADO","PANTALLA"],
        "PORCESO":["HFC","BACKLOG","BACKLOG PYMES","MINTIC","FTTH","PYMES,HHPP"],
        "CUMPLIMIENTO":['Cumple','No cumple'],
        "TIPOORDEN":["Arreglo","Blindaje","Brownfield","Instalacion","postventa","Traslado"],
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
                    "ENRUTAMIENTO"],
        "COMODIN2":[1,2,3,4,5,"N/A"],
        "Tiempos":ArrayRangos
    }

    #return render_template('EleCalidad/plantillaDashboard.html',DicDatForm=DicDatos)
    return render_template('EleCalidad/formEvaluador.html',DicDatForm=DicDatos)

# renderizar historial de monitoreos
#rutas protegidas
@app.route('/HistorialMon')
@login_required
def HistorialMon():
    ArrayCasos= ModelConsultas.GetDataCasoHis(db)
    '''dicDatHis={}
    dic={}
    for i in range(len(x)):
        dic.update({str(i):x[i]})
    ArrayCasos=[dicDatHis]'''

    return render_template('EleCalidad/HistorialMonitoreos.html', arrayGestionH=ArrayCasos)

@app.route('/DetCaso',methods=['POST'])
@login_required
def DetCaso():
    IDCaso = request.get_json()
    ArrayCasos= ModelConsultas.GetDetMon(db,IDCaso['Caso'])

    ArrayItems=ModelConsultas.GetIteMon(db,IDCaso['Caso'])

    dic={}
    for i,j in enumerate(ArrayCasos):
        dic.update({str(i).zfill(2):str(j)})
    dic.update({'items':ArrayItems})
    return jsonify(dic)


##################vistas del orquestador#####################

@app.route('/VistaBotsGes')
@login_required
def VistaBotsGes():
    DicBots=ModelBots.GetAllBots(db)
    DicGen={"Backoffice":[1,2,3],
            "Labor":["Crear","Completar","Marcar Confirmacion","Marcar Demora","Marcar Seguimiento","Marcacion Soporte","Marcacion TAM","Marcacion Multiple","Repara y Actualiza","Actualizar","Marcacion MiN & PY"],
            "Ciudad":["Bogota","Cali"]}
    return render_template('EleOrquestador/ListadoBots.html',DicBotsActivos=DicBots,DicDatOrq=DicGen)


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

app.route("\AppDataBase")
@login_required
def AppDataBase():
    JsonOption = request.get_json()
    if JsonOption['Gestion']=="UpdEstadoBot":
        ModelConsultas.FuncionUpdDel(db,["UPDATE tbl_controlbot SET CTL_CDETALLE1='"+str(JsonOption['NueEstatus'])+"' WHERE CTL_CNOMBOT='"+str(JsonOption['Bot'])+"'"])
        ModelConsultas.FuncionSel(db,["select CTL_CDETALLE1 from tbl_controlbot WHERE CTL_CNOMBOT='"+str(JsonOption['Bot'])+"'"])
    elif JsonOption['Gestion']=="GetCaso":
        print("caso x")




#manejo de errores navegacion
def estatus401(error):
    return redirect(url_for('login'))

def estatus404(error):
    return "<h1>Pagina no encontrada</h1>",404



if __name__=='__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401,estatus401)
    app.register_error_handler(404, estatus404)
    app.run(host="0.0.0.0")
