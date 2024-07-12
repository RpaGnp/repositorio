import datetime
import pandas as pd
import xlwt
from .ModeloItemsMon import ModelConsultas
import csv

class Lector():
    def __init__(self) -> None:
        pass    
    
    
    @classmethod
    def BigDataMonitoreoClaro(self,File):

        #df = pd.read_excel()
        def convert_to_percent_string(value):
            return '{}'.format(value * 100)
        

        df = pd.read_excel(File,header=0, sheet_name='BASE NOTA',converters={'Nota_general_gana': convert_to_percent_string})
        dfITEMS = pd.read_excel(File,header=0, sheet_name='BASE ITEMS')
        #df = pd.read_excel(File, header=0)#, converters={'Nota_calidad_emitida': convert_to_percent_string})


        ArrayGeneral=[]
        for i in df.index:
            dicDatos={}
            dicDatos["Login"]=df["Login"][i]
            dicDatos["Aliado"]=df["Aliado"][i]
            dicDatos["Regional"]=df["regional"][i] 
            dicDatos["FechaMon"]=df["Fecha_monitoreo"][i]# j[0]
            dicDatos["Cuenta"]=df["Cuenta"][i]# j[8]
            dicDatos["Orden"]=df["OT_LLS"][i] #j[9]
            dicDatos["fechaAge"]=df["Fecha_gestion"][i]# j[1]
            dicDatos["TipoOrden"]=df["Motivo_de_ot"][i]# j[10]
            dicDatos['IDLlamada']=df["ID_Llamada"][i]

            ArrayItemsAfec = dfITEMS[dfITEMS['ID_AUDIO'] == dicDatos['IDLlamada']]
            #print(dicDatos['IDLlamada'],ArrayItemsAfec)            
            
            Arraytempitems=[]
            NiteCumple=0
            NiteNoCumple=0
            for j in ArrayItemsAfec.index:
                if ArrayItemsAfec['CALIFICACION'][j]=="Cumple":
                    NiteCumple+=1
                else:
                    NiteNoCumple+=1                
                Arraytempitems.append({ArrayItemsAfec['MACROPROCESO'][j]:ArrayItemsAfec['CALIFICACION'][j]})

            l=df["Observacion"][i]
            ini=l.find("Razón: ")
            fin=l.find("Correcta:")
            Razon=l[ini+(len("Razón: ")):fin]
            dicDatos["Razon"]=Razon	
            del l            
            dicDatos["Observaciones"]=df["Observacion"][i]# j[10]
            dicDatos["Nota"]=df["Nota_general_gana"][i]
            dicDatos["Nec"]=NiteCumple
            dicDatos["Nenc"]=NiteNoCumple
            dicDatos["Nerrores"]=NiteNoCumple

            DicGeneral={"DatosMon":dicDatos,"DatosItems":Arraytempitems}
            ArrayGeneral.append(DicGeneral)
        '''for i in dx.dfITEMS:
                                    DicItems={}
                                    DicItems["idAudio"]=df["ID_AUDIO"][i]
                                    dicDatos["Calificacion"]=df["CALIFICACION"][i]
                                    '''

        return ArrayGeneral

    @classmethod
    def LectorNotasPreturno(self,db,IdPreturno,IdUsuario,file):
        def convert_to_percent_string(value):
            return '{}'.format(value * 100)
        
        DfNotas = pd.read_excel(file,header=0,converters={'NOTA DE EVALUACION ': convert_to_percent_string})        
        for i in DfNotas.index:            
            '''DfNotas["CEDULA"][i]
            DfNotas["NOMBRE"][i]
            DfNotas["FECHA DE ASISTENCIA "][i]
            DfNotas["FECHA DE LA EVALUACION "][i]
            DfNotas["NOTA DE EVALUACION "][i]'''
            datos=[IdPreturno,IdUsuario, DfNotas["CEDULA"][i],DfNotas["FECHA DE ASISTENCIA "][i],DfNotas["FECHA DE LA EVALUACION "][i],round(float(DfNotas["NOTA DE EVALUACION "][i]),2)]
            data = ModelConsultas.FuncGetSPR(db, 1,"spr_get_estasipre",[IdPreturno,DfNotas["CEDULA"][i]])            
            if data!=None:
                ModelConsultas.FuncionUpdDelSpr(db, ["spr_upd_estasipre",datos])
            else:
                ModelConsultas.FuncionUpdDelSpr(db, ["spr_ins_asipre", datos])
        
    @classmethod
    def lectorcsv(self,pathfile):
        with open(pathfile, newline='') as archivo_csv:
            next(archivo_csv)
            lector_csv = csv.reader(archivo_csv,delimiter=";",)
            ArrayDatos=[]
            for fila in lector_csv:
                ArrayDatos.append(fila)
        return ArrayDatos
#Lector.LectorNotasPreturno(280,1070968663,r"C:\Users\USER\Downloads\PLANTILLA YEISON(1).xlsx")


def MakeInf(NameCols,ArrayData,Path):
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Calidad', cell_overwrite_ok=True)
    for i,col in enumerate(NameCols):
        ws.write(0, i, col)

    # for key, value in dicCartas.items():
    #fila = 1
    #columna = 0
    for index,fila in enumerate(ArrayData):
        index+=1
        #print(fila)
        for x,dato in enumerate(fila):
            #print(dato)
            ws.write(index, x, dato)
            '''columna += 1
                                                ws.write(index, columna, value)
                                                columna += 1
                                                ws.write(index, columna, timer()[0], style1)
                                                columna += 1
                                                ws.write(index, columna, timer()[1])
                                                columna = 0'''
        #fila += 1
    
    wb.save(Path)


def generarInformeCsv(pathfile,arrayencabezados,arraydatos):
    with open(pathfile, mode='w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv,delimiter=";")
        escritor_csv.writerow(arrayencabezados)
        for fila in arraydatos:
            escritor_csv.writerow(fila)
    return 1


