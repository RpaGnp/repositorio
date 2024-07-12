import os
from datetime import datetime

def CreadorCarpetas(carpetasegura):
    # A�o
    Pathyear = os.path.join(carpetasegura, datetime.now().strftime("%Y"))
    if not os.path.exists(Pathyear):
        os.mkdir(Pathyear)

    # Mes
    PathMes = os.path.join(Pathyear, datetime.now().strftime("%m"))
    os.chdir(Pathyear)
    if not os.path.exists(PathMes):
        os.mkdir(PathMes)

    # D�a
    pathDia = os.path.join(PathMes, datetime.now().strftime("%d"))
    if not os.path.exists(pathDia):
        os.mkdir(pathDia)

    return pathDia

def CreadorCarpetasFiles(carpetasegura):
	# Año
	Year = datetime.now().strftime("%Y")
	Pathyear = os.path.join(carpetasegura, Year)
	if not os.path.exists(Pathyear):
		os.mkdir(Pathyear)

	# Mes
	Mes =datetime.now().strftime("%m")
	PathMes = os.path.join(Pathyear, Mes)
	os.chdir(Pathyear)
	if not os.path.exists(PathMes):
		os.mkdir(PathMes)

	# Día
	Dia = datetime.now().strftime("%d")
	pathDia = os.path.join(PathMes, Dia)
	if not os.path.exists(pathDia):
		os.mkdir(pathDia)

	return pathDia,f"{Year}/{Mes}/{Dia}"