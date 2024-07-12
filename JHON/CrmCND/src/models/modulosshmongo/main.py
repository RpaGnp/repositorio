import os
import pandas as pd
from .ConsultorMongo import Handledbmongo
from .ConsultorSh import SharePoint
from bson import ObjectId
import datetime
import tempfile

class GestorConsultasshMongo:
    def __init__(self):        
        self.dicolciudad={"Bogota":"ActividadesWFMBogota","Cali":"ActividadesWFMCali","Bucaramanga":"ActividadesWFMBucaramanga"}
        self.colactividades="ActividadesWfmnacional"
        self.histarchivoscargados = "Archivos_cargados"
        self.coleccionAvance= "Avance_operacion"
        self.diccolavancebyciudad = {"Bogota": "Avance_operacion_Bogota","Bucaramanga":"Avance_operacion_Bucaramanga",
                                    "Cali":"Avance_operacion_Cali"}
        


    def timmer(self):
        now = datetime.datetime.now()
        fecha=now.strftime("%Y-%m-%d")
        horas = now.strftime("%H:%M:%S")
        return fecha,horas

    def yearmonth(self):
        now = datetime.datetime.now()
        year=now.year
        month = now.month
        return year, month


    def lectorDf(self,df):
        datos_array = []		
        for indice, fila in df.iterrows():		    
            fila_array = []
            for elemento in fila:
                fila_array.append(elemento)		    
            datos_array.append(fila_array)		
        return datos_array

    def leer_excel_pd(self,file_path,DicdatosUsuario={}):			
        motor = 'openpyxl' if file_path.endswith("xlsx") else 'xlrd'
        datos = pd.read_excel(file_path,engine=motor)
        data = {}	

        Handledbmongo().RemoveData("ActividadesWFMBogota",1)	
        encabezados = list(datos.columns)

        sheet_data = []
        for index,data in enumerate(self.lectorDf(datos)):					
            row_data = {}			
            for col in range(len(encabezados)):
                row_data[encabezados[col]] = data[col]
            if len(DicdatosUsuario)!=0:
                row_data.update(DicdatosUsuario)
            sheet_data.append(row_data)
            
        return 	sheet_data

    def insbasecontrol(self, dicdatos):
        ahora = self.timmer()
        dicControl ={   
            "Id_usuarioregistro":dicdatos['Idasesor'],
            "Ciudad":dicdatos['Ciudad'],
            "Fecha_registro":ahora[0],
            "Hora_registro":ahora[1],
            "Estado_registro":1,
            "Fecha_descativacion":None,
            "Hora_descativacion":None,
            "Estado_base":1,
            "Archivos_Registrados":[]

        }
        IdControl = Handledbmongo().InsertDataOne("control_cargas",dicControl)
        return IdControl
    
    def getfilesupdxmes(self):
        # optener mes actual y pasado
        # consultar en mongo
        # returnar el array
        Ahora = list(self.yearmonth())
        year = Ahora[0]
        months = [Ahora[1], Ahora[1] - 1]
        # Construir la consulta
      

        if Ahora[1]==1:         
            projection = {
                f"{str(year-1)}.{str(12)},{year}.{Ahora[1]}"
            }
        else:            
            projection = {
                f"{str(year)}.{month}": 1 for month in months
            }
        
        projection.update({ '_id': 0})        
        arraydatos=Handledbmongo().GetData(self.histarchivoscargados,{},projection)
        
            
        arrayfiles=[]
        for dic in list(arraydatos[0].values()):
            for mes,arraymes in dic.items():
                arrayfiles+=arraymes
                
        return arrayfiles

    def updfilesxmes(self,arrayupd):
        now = datetime.datetime.now()
        year = now.year
        month=now.month
        filter_query = {str(year): {"$exists": True}}
        update_query = {
            "$push": {
                f"{year}.{month}": {
                    "$each": arrayupd
                }
            }
        }
        
        result =Handledbmongo().UpdDataOne(self.histarchivoscargados ,2,filter_query ,update_query )
        if result.matched_count > 0:
            if result.modified_count > 0:
                return f"Elemento agregado correctamente al mes en el documento."
            else:
                return f"No se realizaron cambios en el documento."
        else:
            return f"No se encontró ningún documento con el año {year}."
        
    def gestorfilesdw(self,dicfiles,Colecionmongo,dicadd={}) :
        dirtempfiles=tempfile.mkdtemp()
        print(dirtempfiles)
        for archivo, values  in dicfiles.items():
            pathFile= os.path.join(dirtempfiles,archivo)            

            with open(pathFile,"wb") as file:
                file.write(values)            
            
            dicadd.update({"ArchivoPadre":archivo})
            datos= self.leer_excel_pd(pathFile,dicadd)            
            if len(datos)!=0:
                Handledbmongo().InsertDataMany(Colecionmongo,datos)
        
    def updAvanceOperacion(self,ciudad):
       # borra los datos de la colexion de la ciudad        
        Handledbmongo().RemoveData(self.diccolavancebyciudad[ciudad],2)
           
        dicarchivos=SharePoint().download_latest_file(ciudad)
        self.gestorfilesdw(dicarchivos,self.diccolavancebyciudad[ciudad])
        print("end download")
        
    def Main(self,idasesor,ciudad):
        self.updAvanceOperacion(ciudad)         
        
        Colecionmongo = self.colactividades 
        # CONSULTAR EL ARRAY DE ARCHIVOS GUARDADOS EN MONGO OPTIMIZAR POR FECHA
        # LA CIONSULTA SE HACE POR AÑO Y MES YA QUE LA ACTIUUALIZACION Y CONSULTA EN 
        # SH SE HACE MES ACTUAL
        # LA CONSULTA SE DEBE HACER MES ACTUIAL Y MES ANTERIOR
        DatosCargados=set(self.getfilesupdxmes())        
        Filesavance = SharePoint().download_all_files() 
        archivossh = set(list(Filesavance.keys()))        
        datosacargar=archivossh.difference(DatosCargados)
        
        #return 1
        idgestion =self.insbasecontrol({"Idasesor":idasesor,"Ciudad":ciudad})
        diccionario_filtrado = {key: value for key, value in Filesavance.items() if key in datosacargar}
        self.gestorfilesdw(diccionario_filtrado,Colecionmongo,{"keycontrol":idgestion})
        
        Handledbmongo().UpdDataOne("control_cargas",1,{"_id":idgestion} , {"Archivos_Registrados":list(diccionario_filtrado.keys())})
        print("En cargas totales")
        return self.updfilesxmes(list(diccionario_filtrado.keys()))
    #print(datos['Hoja1'])




# consultar y contar datos
'''criteriosBusqueda={"ciudad":"Bogota"}
datos=Handledbmongo().GetData("ActividadesWFM",criteriosBusqueda,DicKeys={})
print(datos)'''


class HandleavanceOperacionDiario:
    def __init__(self,ciudad):
        self.ciudad = ciudad.capitalize()
        self.coleccion= "Avance_operacion"

    def delcolciudad(self):
       # borra los datos de la colexion de la ciudad
        query = {self.ciudad: {'$exists': True}}
        update = {'$set': {self.ciudad: []}}
        result = Handledbmongo().updatemany(self.coleccion,query,update)
        print(result)

    def downfilessh(self):
        dicarchivos=SharePoint().download_all_files_avance(self.ciudad)
        

        # solicta la conexion a share potin a la carpeta de la ciudad