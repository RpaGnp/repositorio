from .entities.User import User

class ModelUser():
    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            #sql = """SELECT usu_nid, usu_cemail, usu_cnom,usu_capell, usu_cclavecrm,usu_cperfil,\
            #        usu_csegmento,usu_cestado\
            #        FROM tbl_usuarios 
            #        WHERE usu_cemail = '{}'""".format(user.username)            
            
            
            sql =f"SELECT usu_nid,usu_nid,usu_cclavecrm from `tbl_husuarioscrm` WHERE usu_nid='{user.username}'"
                    
            cursor.execute(sql)
            row = cursor.fetchone()
            cursor.close()
            if row != None:
                try:
                    user = User(row[0],row[1],User.check_password(row[2].decode('UTF-8'),user.password))
                    return user
                except:pass
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def Get_by_id(self, db, Id):
        try:
            cursor = db.connection.cursor()
            #sql = """SELECT usu_nid, usu_cemail, usu_cnom,usu_capell,usu_cclavecrm,usu_cperfil,usu_csegmento,usu_cestado FROM tbl_usuarios 
            #        WHERE usu_nid = '{}'""".format(Id)

            sql = f"SELECT usu_nid,usu_cclavecrm,usu_cnombres,usu_cemail,usu_ccampaña,usu_ccargo,usu_cperfil,usu_csupervisor,\
                    usu_cciudad,usu_dfechingreso,usu_cmuestras,usu_cestado,DATEDIFF(NOW(),usu_dultactclave)\
                    FROM tbl_husuarioscrm\
                    WHERE usu_nid='{Id}'"

            #print(sql)
                    
            cursor.execute(sql)
            row = cursor.fetchone()
            cursor.close()
            if row != None:
                return User(row[0],row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12])
            else:return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def getDatAseMon(self,db,ced):
        cursor = db.connection.cursor()
        cursor.callproc("SPR_GET_DATASEMON",[ced])
        row = cursor.fetchone()
        cursor.close()        
        if row != None:
            return row
        else:return None
    
            
        
    @classmethod    
    def CheckUpdPw(self,db,iduser,pwuser):
        cursor = db.connection.cursor()
        sql=f"select usu_cclavecrm from tbl_husuarioscrm where usu_nid='{iduser}'"
        cursor.execute(sql)
        Pw=cursor.fetchone()[0]
        cursor.close()
        return User.check_password(Pw.decode('UTF-8'),pwuser)

    @classmethod
    def GenPass(self,password):
        return User.GetNewpassword(password)

    @classmethod
    def GetDataUsuario(self, db):
        with db.connection.cursor() as cursor:
            ArrayAsesores = []
            cursor.callproc("SPR_GET_GESUSU")
            for i in cursor.fetchall():
                ArrayAsesores.append({"Id": i[0], "Nombre": i[1], "Email": i[2], "Campaña": i[3], "Cargo": i[4],
                                      "Perfil": i[5], "Supervisor": i[6], "Ciudad": i[7], "FechaIngreso": i[8],
                                      "FechaSalida": i[9], "Login": i[10], "Estado": i[11], "Contraseña": i[12]})
        cursor.close()
        return ArrayAsesores
