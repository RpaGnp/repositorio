from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId


class Handledbmongo:
	def __init__(self,host='172.20.100.51', port=27017, username=None, password=None):

		self.nombreDb = 'db_hinformes_cnd'
		self.client = MongoClient(host,port)

	def Conn(self):
		return self.client[self.nombreDb]

	def DxConn(self):
		self.client.close()	

	def UpdDataOne(self, coll, tipo ,JsonBusq, jsonDatos):
		db = self.Conn()
		collection = db[coll]
		if tipo==1:
			result = collection.update_one(JsonBusq,{"$set":jsonDatos},upsert=True)
		else:
			result =collection.update_one(JsonBusq, jsonDatos)
		self.DxConn()
		return result
	
	def updatemany(self,coll,where,updates):
		db = self.Conn()
		collection = db[coll]
		result = collection.update_many(where, updates)
		self.DxConn()
		return result.modified_count



	def GetData(self, coll,criteriosBusqueda,DicKeys={}):		
		db = self.Conn()
		collection = db[coll]								
		cursor = collection.find(criteriosBusqueda,DicKeys,sort=[('Fecha', -1),('Hora', -1)])	
		documentos = list(cursor)		
		self.DxConn()		
		return documentos	
		
	def GetDatafilesyear(self,coll,year,criteriosBusqueda,DicKeys={}):
		
		db = self.Conn()
		collection = db[coll]
		cursor = collection.find_one({str(year): {"$exists": True}}, criteriosBusqueda)
		documentos = list(cursor)		
		self.DxConn()		
		return documentos


	def InsertDataOne(self, coll, documento):
		db = self.Conn()
		collection = db[coll]
		resultado = collection.insert_one(documento)	    
		self.DxConn()
		return resultado.inserted_id

	def InsertDataMany(self, coll, ArrayDatos):
		db = self.Conn()
		collection = db[coll]
		resultado = collection.insert_many(ArrayDatos)	    
		self.DxConn()
		return resultado
        
	def RemoveData(self,coll,tipo=0,JsonBusq=None):
		db = self.Conn()
		collection = db[coll]
		if tipo == 0:
			collection.delete_one(JsonBusq)
		else:
			collection.delete_many({})
		self.DxConn()



#ArrayDataOt={"Razon":"EQUIPOS CLIENTE NO APTOS/NO DISPONIBLES","OtLls":"396983466_O_CO_26","Id Usuario Cnd":"1001117754","Asesor Cnd":"MANUEL FELIPE MESA DANIELDS","OBSERVACIONES":"Casa de dos pisos, Fachada color café , Puerta blancan254466879915 este es el que tiene físico y este es el que le hace falta 254471120105","null":""}

# ArrayRazonesCancelables = Handledbmongo().GetTrabajosRazon("Bogota",'Blindaje')												
# print(ArrayRazonesCancelables)