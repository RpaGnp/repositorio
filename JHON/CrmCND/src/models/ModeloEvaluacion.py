# -*- coding: utf-8 -*-
import json
import csv

########################
def Extractor(array):
	dic=array
	converted_a = {}
	for item in dic:
		item=json.loads(item)		
		for dic in item:
			for key, value in dic.items():
				converted_a[key] = value	
	return converted_a

def CalNotaEva(ArrayFormador,ArrayAsesor):	
	DicFormador=Extractor(ArrayFormador)
	# calcular el peso de las preguntas
	RespAsesor=ArrayAsesor
	PesoPreguntas = round(100/len(RespAsesor),2)	
	porcentajeAcierto=0	
	for dic in RespAsesor:

		RespuestasFormador = DicFormador[dic['IdPregunta']]['ResPre']
		RespuestasAsesor=    dic['RespAsesor']
		TipoRespuesta = DicFormador[dic['IdPregunta']]['TipoPregunta']
		

		if TipoRespuesta !='3b':			
			porcentajeAcierto += PesoPreguntas if RespuestasAsesor == RespuestasFormador else 0
		else:
			# ordenar
			PorcentajeRespuesta= round(PesoPreguntas/len(dic['RespAsesor']),2)		
			for clave,valor in RespuestasAsesor.items():			
				porcentajeAcierto += PorcentajeRespuesta if int(RespuestasFormador[clave]) == int(RespuestasAsesor[clave]) else 0

	return round(float(porcentajeAcierto),1)


def createcsvrespuestas(ArrayDatos, UbicacionFile):
	DicDatosAsesor = json.loads(ArrayDatos[1])
	DataFormador = json.loads(ArrayDatos[0])

	# print(DataFormador)
	# print(DicDatosAsesor)
	def GetDicAsesor(IdPregunta):
		for x in DicDatosAsesor:
			if x['IdPregunta'] == IdPregunta:
				return x

	def GetAnsCorrect(DicRespuestas):
		arrayCorrect = []
		for x, y in DicRespuestas.items():
			if y == True:
				arrayCorrect.append(x)
		return arrayCorrect

	with open(UbicacionFile, "w", newline='', encoding='utf-8') as csvfile:
		fieldnames = ['IdPregunta', 'Pregunta', "RespuestaCorrecta", "RespuestaAsesor"]
		writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
		writer.writeheader()

		for i in DataFormador:
			for x, y in i.items():
				dicRespAsesor = GetDicAsesor(x)
				# print(dicRespAsesor)
				Pregunta = y['Pregunta']
				RespCorrecta = GetAnsCorrect(y['ResPre'])
				RespAse = GetAnsCorrect(dicRespAsesor['RespAsesor'])
				writer.writerow({'IdPregunta': x, 'Pregunta': Pregunta, 'RespuestaCorrecta': RespCorrecta,
								 'RespuestaAsesor': RespAse})


class InformesMasivo:
	def __init__(self, BigArray):
		self.BigArray = BigArray
		self.ArrayFormador = self.GetArrayFormacion()
		self.ArrayEncabezados = ['Cedula', 'Nombre', 'Campaña', 'Supervisor', 'IdPreturno', 'Asistencia',
								 'FechaAsistencia',
								 'HoraAsistencia', 'Evaluacion', 'FechaEavaluacion', 'HoraEvaluacion',
								 'Nota'] + self.GetNomPreguHead()

	def GetArrayFormacion(self):
		ArrayRespFormador = None
		for i in self.BigArray:
			ArrayRespFormador = json.loads(i[12])
			break
		return ArrayRespFormador

	def GetNomPreguHead(self):
		ArrayPreguntas = []
		for dic in self.ArrayFormador:
			for key, value in dic.items():
				ArrayPreguntas.append(value['Pregunta'])
		return ArrayPreguntas

	def AddNomPre(self, ArrayAsesor):
		'''
			agregar al aray de asesor el nombre de la pregunta
		'''
		for i in ArrayAsesor:
			i["Pregunta"] = self.getNomPre(i['IdPregunta'])

	def getNomPre(self, idpreg):
		for index, dic in enumerate(self.ArrayFormador):
			for idpredunta, inforPregunta in dic.items():
				if idpreg == idpredunta:
					return inforPregunta['Pregunta']

	def GetAnsCorrect(self, DicRespuestas):
		arrayCorrect = []
		for x, y in DicRespuestas.items():
			if y == True:
				arrayCorrect.append(x)
		return arrayCorrect

	def Main(self, UbicacionFile):
		with open(UbicacionFile, "w", newline='', encoding='utf-8') as csvfile:
			writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=self.ArrayEncabezados)
			writer.writeheader()
			for i in self.BigArray:
				ArrayMain = []
				for dic in json.loads(i[13]):  # array de preguntas respondidas por asesor
					dic['Pregunta'] = self.getNomPre(dic['IdPregunta'])
					ArrayMain.append(dic)

				dictemp = {}
				for dic in ArrayMain:
					dictemp[dic['Pregunta']] = self.GetAnsCorrect(dic['RespAsesor'])
				# print(dictemp)
				# break

				dataSave = {'Cedula': i[0], 'Nombre': i[1], 'Campaña': i[2], 'Supervisor': i[3], 'IdPreturno': i[4],
							'Asistencia': i[5], 'FechaAsistencia': i[6],
							'HoraAsistencia': i[7], 'Evaluacion': i[8],
							'FechaEavaluacion': i[9], 'HoraEvaluacion': i[10], 'Nota': i[11],
							}

				dataSave.update(dictemp)
				writer.writerow(dataSave)





