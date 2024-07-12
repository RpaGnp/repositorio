class Config:
    SECRET_KEY='4R34Rp4-GNP-CND_2022'


class DevelopmentConfig(Config):
    DEBUG=True
    #MYSQL_HOST='172.19.101.83' #'190.60.100.100'
    MYSQL_HOST =  '190.60.100.100'
    MYSQL_USER='BotCndCen'
    MYSQL_PASSWORD="B0tCndC3n24*"
    MYSQL_DB="dbcrmcalv2"




config={
    'development':DevelopmentConfig


}