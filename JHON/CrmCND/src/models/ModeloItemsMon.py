

class ModelConsultas():
    
    
    
    @classmethod
    def GetDataFormMon(self, db, Campaña):
        try:
            cursor = db.connection.cursor()
            '''print(Campaña)
            if Campaña not in ["BACKLOG"]:
                Campaña="BACKLOG"
            else:
                Campaña="DESPACHO"'''
            #print(Campaña)
            if Campaña.upper() in ["DESPACHO","BACKLOG"]:
                cursor.callproc("SPR_GET_ITEMFORM",[Campaña])
            else:
                cursor.callproc("spr_get_itemhp")
            
            row = cursor.fetchall()
            #print(row)
            cursor.close()
            #db.connection.close()#pato
            if row != None:
                try:
                    return row
                except:pass
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
            

    @classmethod
    def InsDataForm(self,db,ArrayDatos):
        try:
            cursor = db.connection.cursor()            
            cursor.callproc("INS_NUEMON",ArrayDatos[0])
            db.connection.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            row = cursor.fetchone()             
            if row != None:
                for i in ArrayDatos[1]:
                    cursor.callproc("INS_FOMSEG",[i['IdItem'],i['Calificacion'],row[0]])
                    db.connection.commit()                    
                cursor.close()
                return row[0]
            
            else :
                cursor.close()
                return None
        except Exception as ex:
            print(ex)
            cursor.close()
            return None
    
    @classmethod
    def InsDataFormMasv(self,db,ArrayDatos):
        cursor = db.connection.cursor()
        #print(ArrayDatos[0])
        cursor.callproc("INS_NUEMON",ArrayDatos[0])
        db.connection.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        row = cursor.fetchone()
        cursor.close()
        if row != None:
            for i in ArrayDatos[1]:
                cursor.callproc("INS_FOMSEG",[i['IdItem'],i['Calificacion'],row[0]])
                db.connection.commit()
            return row[0]
        else:
            return None
    

    @classmethod
    def GetDataCasoHis(self,db,idasesor):
        try:
            cursor = db.connection.cursor()
            cursor.execute(f"SELECT usu_ccargo,usu_cciudad FROM tbl_husuarioscrm WHERE usu_nid='{idasesor}'")            
            perfil = cursor.fetchone()                        
            if perfil[0]=="ASESOR":
                cursor.callproc('spr_get_cmonxase',[idasesor])
            elif perfil[0]=="SUPERVISOR":
                cursor.callproc("SPR_GET_MONXSUP",[idasesor])
            elif perfil[0]=="LIDER CALIDAD":
                cursor.execute(f"select * from casosmonitoreos")           
            else:
                cursor.execute(f"select * from casosmonitoreos where ase_cciudad='{perfil[1]}'")           
            
            row=cursor.fetchall()            
            cursor.close()
            if row != None:
                return row
            else:
                return None
        except Exception as ex:
            print(ex)
            return None

    @classmethod
    def GetDetMon(self,db,caso):
        try:
            cursor = db.connection.cursor()
            cursor.callproc("SPR_GET_DETCASMON",[caso])
            row = cursor.fetchone()
            cursor.close()

            '''cursor.callproc("SPR_GET_ITEMSAFECXMON",[caso])
            rowItems = cursor.fetchall()
            print(rowItems)'''

            if row != None:
                return row
            else:
                return None
        except Exception as ex:
            print(ex)
            return None

    @classmethod
    def GetIteMon(self,db,caso):
        try:
            cursor = db.connection.cursor()
            cursor.callproc("SPR_GET_ITEMSAFECXMON",[caso])
            rowItems = cursor.fetchall()
            cursor.close()
            if rowItems != None:
                return rowItems
            else:
                return None
        except Exception as ex:
            print(ex)
            return None

    @classmethod
    def FuncionGetSPR(self, db, consulta):
        with db.connection.cursor() as cursor:
            # print(len(consulta))
            if len(consulta) > 1:
                cursor.callproc(consulta[0], args=(consulta[1],))
            else:
                cursor.callproc(consulta[0])
            data = cursor.fetchall()
        cursor.close()
        return data

    @classmethod
    def FuncGetSPR(self, db,tipo,consulta,array=None):
        with db.connection.cursor() as cursor:
            if array!=None:
                cursor.callproc(consulta, args=(array))
            else:
                cursor.callproc(consulta)
            if tipo==1:
                data = cursor.fetchone()
            else:
                data = cursor.fetchall()
        cursor.close()
        return data

    @classmethod
    def FuncionUpdDel(self, db, consulta):
        with db.connection.cursor() as cursor:
            # print(len(consulta))
            if len(consulta) > 1:
                cursor.execute(consulta[0], args=(consulta[1]))
            else:
                cursor.execute(consulta[0])
            db.connection.commit()
        cursor.close()
        return True

    @classmethod
    def FuncionSel(self, db, consulta):
        with db.connection.cursor() as cursor:
            # print(len(consulta))
            if len(consulta) > 1:
                cursor.execute(consulta[0], args=(consulta[1]))
            else:
                cursor.execute(consulta[0])
            data = cursor.fetchall()
        cursor.close()
        return data

    @classmethod
    def FuncionUpdDelSpr(self, db, consulta):
        with db.connection.cursor() as cursor:
            #print(consulta)
            if len(consulta[1]):
                if type(consulta[1])==list:
                    Arg=[]
                    for i in consulta[1]:
                        Arg.append(i)
                else:
                    Arg=[consulta[1]]

                cursor.callproc(consulta[0], args=(Arg))
            else:
                cursor.callproc(consulta[0])
            #print(Arg)
            db.connection.commit()
        cursor.close()
        return True
    
    @classmethod
    def FuncionIns(self, db, consulta):
        with db.connection.cursor() as cursor:
            #print(consulta)
            if len(consulta[1]):
                if type(consulta[1])==list:
                    Arg=[]
                    for i in consulta[1]:
                        Arg.append(i)
                else:
                    Arg=[consulta[1]]
                cursor.callproc(consulta[0], args=(Arg))
            else:
                cursor.callproc(consulta[0])
            db.connection.commit()

            cursor.execute("SELECT LAST_INSERT_ID()")
            row = cursor.fetchone()
            cursor.close()
        
        return row
    
    @classmethod
    def FuncionInsSpr(self, db, consulta):
        with db.connection.cursor() as cursor:
            #print(consulta)
            if len(consulta[1]):
                if type(consulta[1])==list:
                    Arg=[]
                    for i in consulta[1]:
                        Arg.append(i)
                else:
                    Arg=[consulta[1]]                
                cursor.callproc(consulta[0], args=(Arg))
            else:
                cursor.callproc(consulta[0])
            db.connection.commit()
        cursor.close()
        return True
    
    @classmethod
    def FuncionGetSprInf(self, db, consulta):
        with db.connection.cursor() as cursor:
            #print(consulta)
            if len(consulta[1]):
                if type(consulta[1])==list:
                    Arg=[]
                    for i in consulta[1]:
                        Arg.append(i)
                else:
                    Arg=[consulta[1]]                
                cursor.callproc(consulta[0], args=(Arg))
            else:
                cursor.callproc(consulta[0])            
            data=cursor.fetchall()
        cursor.close()
        return data
    
    
    
    @classmethod
    def InsCargaClaro(self,db,ArrayDatos):
        cursor = db.connection.cursor()
        cursor.callproc("INS_NUEMON",ArrayDatos)
        db.connection.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        row = cursor.fetchone()
        cursor.close()
        return row[0]
    

    
    @classmethod
    def CargaItemsClaro(self,db,dicDATOS,Idregistro,idasesor):
        with db.connection.cursor() as cursor:
            cursor.execute(f"select usu_ccampaña from tbl_husuarioscrm where usu_nid='{idasesor}'")
            camAse=cursor.fetchone()[0]
            if "BACKLOG" in camAse:
                camAse="BACKLOG"  
            else:
                camAse="DESPACHO"
        cursor.close()

        for dicItem in dicDATOS:
            for item, calificacion in dicItem.items():
                cursor = db.connection.cursor()
                print("!",item.strip(), camAse)
                cursor.callproc("SPR_GET_IDITEMBYNAME", args=(item.strip(), camAse))
                idItem=cursor.fetchone()
                idItem=idItem[0]
                cursor.close()

                cursor = db.connection.cursor()
                cursor.callproc("INS_FOMSEG",[idItem,calificacion,Idregistro])
                db.connection.commit()
                cursor.close()
    
    @classmethod
    def GestorItems(self,db,idmon):
        Cumpe,NoCumple="",""
        with db.connection.cursor() as cursor:            
            cursor.callproc("spr_get_calitem",args=([idmon]))
            for x in cursor.fetchall():
                if  x[1]=="Cumple":
                    Cumpe+=f"{x[0]}, "
                elif x[1]=="No cumple":
                    NoCumple+=f"{x[0]}, "

        #cursor.close()        
        #db.connection.close()
                       
        return Cumpe,NoCumple

    def FuncGetSpr(db,tipo, procedimiento, Arraydatos=[]):
        data = []
        with db.connection.cursor() as cursor:
            if len(Arraydatos) != 0:
                cursor.callproc(procedimiento, args=(Arraydatos))
            else:
                cursor.callproc(procedimiento)
            if tipo == 1:
                data = cursor.fetchone()
            else:
                data = cursor.fetchall()
        return data