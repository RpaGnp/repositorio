from pymongo import MongoClient
from datetime import datetime
#from bson import ObjectId

class Handledbmongo:
	def __init__(self,nombreDb='NotificacionesCnd'):		
		self.nombreDb = nombreDb
		self.client = MongoClient(host='172.20.100.51', port=27017)

	def Conn(self):
		return self.client[self.nombreDb]

	def DxConn(self):
		self.client.close()

	def UpdDataOne(self, coll, JsonBusq, jsonDatos):
		db = self.Conn()
		collection = db[coll]
		collection.update_one(JsonBusq,{"$set":jsonDatos},upsert=True)
		self.DxConn()
	        # Hacer operaciones de actualización aquí

	def GetData(self, coll,JsonBusq={},DicKeys={}):		
		db = self.Conn()
		collection = db[coll]						
		cursor = collection.find(JsonBusq,DicKeys,sort=[('Fecha', -1),('Hora', -1)])	
		documentos = list(cursor)		
		self.DxConn()		
		return documentos

	def InsertDataOne(self, coll, documento):
		db = self.Conn()
		collection = db[coll]
		resultado = collection.insert_one(documento)	    
		self.DxConn()
		return resultado.inserted_id
        
	def RemoveData(self,coll,tipo=0,JsonBusq=None):
		db = self.Conn()
		collection = db[coll]
		if tipo == 0:
			collection.delete_one(JsonBusq)
		else:
			collection.delete_many({})
		self.DxConn()


#print(Handledbmongo("BotCND").GetData("DicRazones",{},{"_id":0}))

class HandleNotificaciones:
	def __init__(self):
		self.codArea={
			1000:"Calidad",
			1001:"Formacion",
			1002:"Operacion"

		}

		self.codSeg={
			"MASIVO":1040,			
			"HHPP":1041,

		}


		self.DicTipoNotificacion={"Calidad":
				{
				1010:"Monitoreo Calidad",
				1011:"Nueva actualizacion calidad",
				1012:"Cierre monitoreo",                        
				1013:"Nueva remocion"
				},
				"Formacion":{
				1020:"Nuevo material de estudio",
				1021:"Nueva Evaluacion",
				1022:"Asistencia evaluacion actualizada"
				},
				"Operacion":{
				1030 :"Error Razonador"
				}
		}
		

		self.DiccodCalor ={
				1100:"icon-circle bg-primary",
				1101:"icon-circle bg-warning",
				1102:"icon-circle bg-danger"
		}


		self.DicLogos={
			1200:"fas fa-edit text-white"
			}

		self.CodRuta ={
			1300:"/Enrrutador/VerPreturno",
			1301:"/HistorialMon"  
		}

	def Timmer(self):
		FechaHora=datetime.now()
		self.Fecha = FechaHora.strftime('%d/%m/%Y')
		self.Hora = FechaHora.strftime('%H:%M:%S')
		return self.Fecha, self.Hora

	def Creator(self,IdUsuario,CodSegmento,CodArea,CodNombre,Detalle,CodCalor,CodIcono,CodRuta):
		Ahora = self.Timmer()
		return {
			"Usuario":IdUsuario,
			"Segmento":	CodSegmento,		
			"Area":self.codArea[CodArea],
	        "Fecha":Ahora[0],
	        "Hora":Ahora[1],
	        "Nombre":self.DicTipoNotificacion[self.codArea[CodArea]][CodNombre],
	        "Detalle":Detalle,
	        "Estado":0,
	        "Calor":self.DiccodCalor[CodCalor],
	        "Icono":self.DicLogos[CodIcono],        
	        "Salida":self.CodRuta[CodRuta]
    	}

	def CheckNotificacionesGobales(self,Coll):		
		return Handledbmongo().GetData(Coll,{"Usuario":99999})

	def CheckNotificacionesUsuario(self,coll,Usuario):
		return Handledbmongo().GetData(coll,{"Usuario":Usuario})

	def ConvertId(self,ArrayNotificaciones):
		for dic in ArrayNotificaciones:        
			dic['_id']=str(dic['_id'])
		return ArrayNotificaciones
	
'''z= HandleNotificaciones().Creator(99999,1000,1010,"Afectacion calidad",1102,1200,1300)

Handledbmongo().InsertDataOne('NotificacionGlobalBogota',z)'''


'''z= HandleNotificaciones()
y = z.CheckNotificacionesGobales('NotificacionGlobalBogota')
x=  z.CheckNotificacionesUsuario(1070968663)
print(y,x)'''

import math

def replace_nan_with_none(data):
    if isinstance(data, dict):
        return {k: replace_nan_with_none(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_nan_with_none(i) for i in data]
    elif isinstance(data, float) and math.isnan(data):
        return None
    else:
        return data