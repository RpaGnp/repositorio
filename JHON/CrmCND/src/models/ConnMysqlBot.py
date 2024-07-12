import pymysql
import datetime
from getpass import getuser
from datetime import date
from datetime import datetime
import platform



class ConectorDbMysql(object):	
    def __init__(self,ciudad):
        self.ciudad = ciudad
        self.conn = False		
        if ciudad.lower() == "cali":
            db_config={'host':'10.206.170.19', 'user':'BotCndCali', 'password':'B0tCndC4Li24*', 'db':'dbcrmgnp'}
        else:
            db_config={'host':'190.60.100.100', 'user':'BotCndCen', 'password':'B0tCndC3n24*', 'db':'dbcrmgnp'}

        self.conn = pymysql.connect(host=db_config['host'],user=db_config['user'],password=db_config['password'],db=db_config['db'])

    def GetConn(self):
        return self.conn

    def GetCursor(self):
        return self.conn.cursor()

    def timer(self):
        FechaHora = datetime.now()	
        date_actual=FechaHora.strftime('%d/%m/%Y %H:%M:%S')
        Fecha = FechaHora.strftime('%d/%m/%Y')
        Hora = FechaHora.strftime('%H:%M:%S')
        fecha = str(Fecha)
        hora = str(Hora)
        return fecha, hora, date_actual,Fecha,Hora

    def dicaasesor(self, arrayasesor):
        dic = {}
        for j in arrayasesor:
            dic[j[0]] = j[1]

        return dic

    def upload(self,user=None,procedimiento=None,PathFile=None,ArrayDatos=[],ArrayaAsesores=[]):
        ## usar solo para carga de datos a base de datos esta fatal no se puede reutilizar , gaaaaaaaazzzzzz
        dicAsesores = self.dicaasesor(ArrayaAsesores)
        conn=self.GetConn()
        cursor=conn.cursor()        
        cursor.callproc("spr_ins_asigback",[user,PathFile,len(ArrayDatos),self.ciudad])
        conn.commit()
        idgestion=cursor.fetchone()[0]
        for row in ArrayDatos:                        
            if user is not None:
                row.insert(0,idgestion)
            row.append(dicAsesores[int(row[-1])])
            try:
                cursor.callproc(procedimiento,row)
                conn.commit()
            except Exception as e:
                print(e)
                conn=self.GetConn()
                cursor=conn.cursor()
        cursor.close()
        conn.close()

