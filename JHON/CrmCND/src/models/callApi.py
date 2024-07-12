import requests
import json


class ConsultorApi:
    def __init__(self):
        self.server="http://190.60.100.100:5700"
        #self.server="http://190.60.100.100:5700"
        #self.server = "http://172.19.101.83:5700"
        #self.server = "http://172.20.100.51:8000"
        self.ApiGet = f'{self.server}/api/v.1/ApiCnd/GetData'
        self.ApiUpd = f'{self.server}/api/v.1/ApiCnd/UpdData'
        self.ApiUpdGet = f'{self.server}/api/v.1/ApiCnd/UpdGetData'


    def callGet(self,dicdatos):
        response = requests.post(self.ApiGet, json=dicdatos)
        data = json.loads(response.text)
        if 'Datos' in data:
            return data['Datos']
        else:
            return data

    def callUpd(self, dicdatos):
        response = requests.post(self.ApiUpd, json=dicdatos)
        data = json.loads(response.text)
        

    def FuncUpdGetSpr(self, dicdatos):
        response = requests.post(self.ApiUpdGet, json=dicdatos)
        data = json.loads(response.text)
        return data['Datos']

#ConsultorApi().callUpd({'servicio': 'BotServer', 'ciudad': 1, 'tipo': 1, 'procedimiento': 'spr_ins_datdxrx', 'arraydatos': [13495, '376964951', 'CLARO', 'LENGUAZAQUE', '24/03/2026', 'OTS']})
#arraypermiso=ConsultorApi().callGet({'servicio': 'Koala', 'ciudad': 1, "tipo": 1, "procedimiento": "spr_get_horlogAse","arraydatos":[1070968663]})
#print(arraypermiso)