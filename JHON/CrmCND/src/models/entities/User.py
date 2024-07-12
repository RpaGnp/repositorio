from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self,id,username, password, nombre=None,email=None,campaña=None,cargo=None,perfil=None,supervisor=None,
                 ciudad=None,fechaingreso=None,muestras=None,estado=None,diasactpw=None) -> None:        
        
        ArrayTipos=[id,username,password, nombre,email,campaña,cargo,perfil,supervisor,ciudad,fechaingreso,muestras,estado,diasactpw]
        '''for i,j in enumerate(ArrayTipos):                        
                                            print(type(j))
                                            if type(j)==tuple:                
                                                ArrayTipos[i]=j[0]'''        
        #
        self.id = ArrayTipos[0]
        self.username=ArrayTipos[1]
        self.password=ArrayTipos[2]
        self.nombre=ArrayTipos[3]
        self.email=ArrayTipos[4]
        self.campaña=ArrayTipos[5]
        self.cargo=ArrayTipos[6]
        self.perfil=ArrayTipos[7]
        self.supervisor=ArrayTipos[8]
        self.ciudad=ArrayTipos[9]
        self.fechaingreso=ArrayTipos[10]
        self.muestras=ArrayTipos[11]
        self.estado=ArrayTipos[12]
        self.diasactpw=ArrayTipos[13]
        
        del ArrayTipos

        #print("*",self.id,self.username,self.password,self.nombre,self.email,self.campaña,self.cargo,self.perfil,self.supervisor,self.ciudad,self.fechaingreso,self.muestras,self.estado ,self.diasactpw)


    @classmethod
    def check_password(self,hashedPassword,Password):
        return check_password_hash(hashedPassword,Password)

    @classmethod
    def GetNewpassword(self,Password):
        return generate_password_hash(Password)
#x=User(0,1234,1234)

#print(generate_password_hash("1234"))

#print(check_password_hash('pbkdf2:sha256:260000$t2SYsw7VqaFM5lSj$de788e453be103ccf6344591b9f9c98f5c869b025e3487d3e7808fd9651bc08f',"1234"))