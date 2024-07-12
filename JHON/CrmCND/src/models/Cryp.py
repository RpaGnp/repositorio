import cryptocode


key="4R34Rp4-GNP-CND_2023"

class GestorEnccycode():
    @classmethod
    def encripcode(self,string):
        str_encoded = cryptocode.encrypt(string,key)
        return str_encoded

    @classmethod
    def decripcode(self,string):
        ## And then to decode it:
        if string!=None:
            str_decoded = cryptocode.decrypt(string,key)            
            return str_decoded
        else:
            return None

import base64

def EncriptarFile():
    file=r"C:\DBGestionBot\DbBotRen.db"
    data = open(file, "rb").read()
    encoded = base64.b64encode(data)
    data_plano=str(encoded)
    dato_encriptado = GestorEnccycode.encripcode(data_plano)


    dato_encriptado=dato_encriptado.encode('ascii')
    decoded = base64.b64decode(dato_encriptado)
    file_name=file
    with open(file_name,"wb") as f:
        f.write(decoded)

    print("Archivo encriptado")

def desencriptar():
    file = r"C:\DBGestionBot\DbBotRen.db"
    data = open(file, "rb").read()    
    data_plano=str(data)
    #decoded = base64.b64decode(data_plano)
    #dato_encriptado = GestorEnccycode.decripcode(decoded)
    print(data_plano)

    dato_encriptado=dato_encriptado.encode('ascii')
    '''decoded = base64.b64decode(dato_encriptado)
                file_name=file
                with open(file_name,"wb") as f:
                    f.write(decoded)'''

#desencriptar()