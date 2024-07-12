from .entities.Bots import Bot

class ModelBots():
    @classmethod
    def GetAllBots(self,db):
        query="SELECT CTL_NIDBOT,CTL_CNOMBOT,CTL_DFECACT,CTL_DHORAACT,CTL_NIDACTIVIDAD\
                FROM tbl_controlbot ORDER BY(CTL_CNOMBOT)"

        cursor = db.connection.cursor()
        cursor.execute(query)
        DicBotsActs={}
        row = cursor.fetchall()
        cursor.close()
        if row != None:
            for i,j in enumerate(row):
                if j[4]!=None:
                      cursor = db.connection.cursor()
                      cursor.callproc("SPR_GETINFOBOT",[j[4]])
                      DataActBot=cursor.fetchone()
                      cursor.close()
                      BotConsulta = Bot(DataActBot[0],DataActBot[1],DataActBot[2],DataActBot[3],
                                    DataActBot[4],DataActBot[5],DataActBot[6],DataActBot[7],DataActBot[8].decode('utf-8'),DataActBot[9],
                                    DataActBot[10])
                else:
                    BotConsulta = Bot(j[0],j[1],j[2],j[3],"--","--","--","--","--","--","--")
                DicBotsActs.update({str(i):BotConsulta})
            

            
            return DicBotsActs
        else:
            return None



    @classmethod
    def FuncionGetSPR(self,db,consulta):
        with db.connection.cursor() as cursor:
            #print(len(consulta))
            if len(consulta)>1:
                cursor.callproc(consulta[0],args=(consulta[1]))
            else:
                cursor.execute(consulta[0])
            data=cursor.fetchall()
        cursor.close()
        return data

    
