import os
import json
import base64
from .modeloCarpetas import CreadorCarpetasFiles



class HandleFiles():
    def __init__(self,MainFolder,ArrayDatos):
        self.ArrayDatos =ArrayDatos
        self.MainFolder =MainFolder
        


    def makefolder(self):        
        PathsFile = CreadorCarpetasFiles(self.MainFolder)                
        for json in self.ArrayDatos:            
            for j in json.values():	
                if 'Files' in j:
                    FileName = j['Files']['NombreFile']
                    base64_data = j['Files']['BinarioFile'].split(",")[1]
                    binary_data = base64.b64decode(base64_data)
                    FolderNameFile =PathsFile[0]+"/"+FileName
                    with open(FolderNameFile,"wb") as f:
                        f.write(binary_data)
                    j['Files']['BinarioFile'] = f"{PathsFile[1]}/{FileName}"
        return self.ArrayDatos


        '''file_content = request.get_json()['file']
        file_name = request.get_json()['name']
        base64_data = file_content.split(',')[1]  # Quitar la parte 'data:image/png;base64,'

        binary_data = base64.b64decode(base64_data)    
        with open(file_name,"wb") as f:
        f.write(binary_data)'''