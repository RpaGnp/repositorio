from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin


class Bot():
    def __init__(self, idBot, nombreBot,  FechaAct,HoraAct,IdActBot,TipGestion,ciuGestion,linGestion,UsuGes,Detges,estGes) -> None:
        self.idBot=idBot
        self.nombreBot=nombreBot        
        self.FechaAct=FechaAct
        self.HoraAct=HoraAct
        self.IdActBot=IdActBot        
        self.TipGestion=TipGestion
        self.ciuGestion=ciuGestion
        self.linGestion=linGestion
        self.UsuGes=UsuGes
        self.Detges=Detges
        self.estGes=estGes
        
        #print("*",self.id,self.username,self.password,self.fullname,self.perfil,self.segmento,self.estado)


    @classmethod
    def GetLaborActBot(self):
        return check_password_hash(hashedPassword,Password)
