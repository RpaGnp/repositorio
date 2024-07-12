import json

# coding=utf8
def CalNotaMon(valores):
	#print(valores)

	DicNotas={"G":{"Cumple":0,"No cumple":0,"No aplica":0,"Ponderacion":0.20},
			  "A1":{"Cumple":0,"No cumple":0,"No aplica":0,"Ponderacion":0.25},
			  "N":{"Cumple":0,"No cumple":0,"No aplica":0,"Ponderacion":0.35},
			  "A2":{"Cumple":0,"No cumple":0,"No aplica":0,"Ponderacion":0.20}}

	TotItemNoCumple=0
	TotItemCumple=0
	for i in valores.values():
		for j in i:
			if j['Calificacion'] == "No cumple":
				TotItemNoCumple += 1
			elif j['Calificacion'] == "No aplica":
				continue
			else:
				TotItemCumple += 1
			DicNotas[j['Item']][j['Calificacion']] +=1

	DicCal = {}
	for key, valor in DicNotas.items():
		divide = (valor['Cumple'] + valor['No cumple'])
		if divide == 0:
			divide=1

		Ponderado = valor['Cumple'] / divide * valor['Ponderacion'] * 100

		DicCal.update({key: Ponderado})
	NotTotal = 0.0
	for i in DicCal.values():
		#print(round(i,1))
		NotTotal += round(i,1)
	#print(NotTotal)
	return TotItemNoCumple,TotItemCumple,NotTotal
	#print(NoCumpleProcesos,	NoCumpleCriticos ,	NoCumpleGenerales,"===",CumpleProcesos,	CumpleCriticos,	CumpleGenerales)
	#return True #[NoCumpleCriticos ,NoCumpleProcesos+NoCumpleGenerales,NoCumpleCriticos+NoCumpleProcesos+NoCumpleGenerales, TotalPon,ItemAfec]
	#return [contadorCriticos ,contadorNoCriticos, contadorCriticos+contadorNoCriticos,ResPro,ItemAfec]

#print(cumple70,cumple30,cumple0,Nocumple70,Nocumple30,Nocumple0)


#x={'datos': [{'IdItem': '37', 'Item': 'Realiza acompañamiento al cliente evitando abandono de la llamada', 'Peso': '0', 'Precicion': 'CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '38', 'Item': 'Realiza devolución de llamada en caso de caída', 'Peso': '0', 'Precicion': 'CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '39', 'Item': 'Trata al cliente con respeto', 'Peso': '0', 'Precicion': 'CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '40', 'Item': 'Uso correcto del canal', 'Peso': '0', 'Precicion': 'CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '41', 'Item': 'Hace uso del token para reprogramar/cancelar visita', 'Peso': '0', 'Precicion': 'CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '42', 'Item': 'Realiza contacto con el cliente', 'Peso': '0', 'Precicion': 'CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '43', 'Item': 'Garantiza el cumplimiento de los compromisos adquiridos con el cliente', 'Peso': '0', 'Precicion': 'CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '44', 'Item': 'Reprograma o cancela visita con autorización y contacto al cliente', 'Peso': '0', 'Precicion': 'CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '45', 'Item': 'Programa visita según lo acordado con el cliente', 'Peso': '0', 'Precicion': 'CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '46', 'Item': 'Garantiza permisos de administración', 'Peso': '0', 'Precicion': 'CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '47', 'Item': 'Realiza preguntas que permitan dar solución al requerimiento del cliente', 'Peso': '0.3', 'Precicion': 'NO CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '48', 'Item': 'Invita al cliente a usar el APP', 'Peso': '0.3', 'Precicion': 'NO CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '49', 'Item': 'Cumple tiempos de gestión', 'Peso': '0.3', 'Precicion': 'NO CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '50', 'Item': 'Cumple tiempos de seguimiento', 'Peso': '0.3', 'Precicion': 'NO CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '51', 'Item': 'Garantiza marcar la razón en RR', 'Peso': '0.3', 'Precicion': 'NO CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '52', 'Item': 'Registra notas de forma completa y correcta', 'Peso': '0.3', 'Precicion': 'NO CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '53', 'Item': 'Confirma motivo de la creación de la OT/LLS', 'Peso': '0.3', 'Precicion': 'NO CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '54', 'Item': 'Brinda información completa y correcta', 'Peso': '0.7', 'Precicion': 'NO CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '55', 'Item': 'Escucha activa', 'Peso': '0.7', 'Precicion': 'NO CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '56', 'Item': 'Tiempos de espera', 'Peso': '0.7', 'Precicion': 'NO CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '57', 'Item': 'La solución atiende la necesidad del cliente', 'Peso': '0.7', 'Precicion': 'NO CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '58', 'Item': 'Actualiza correo y teléfonos de contacto del cliente para el envío del token', 'Peso': '0.7', 'Precicion': 'NO CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '59', 'Item': 'Uso adecuado de suspensión de eventos', 'Peso': '0.7', 'Precicion': 'NO CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '60', 'Item': 'Confirma dirección del evento', 'Peso': '0.7', 'Precicion': 'NO CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '61', 'Item': 'Genera solicitud para replanteamiento/ampliación de tap', 'Peso': '0.7', 'Precicion': 'NO CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '62', 'Item': 'Realiza seguimiento a eventos razonados por R y H', 'Peso': '0.7', 'Precicion': 'NO CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '63', 'Item': 'Amabilidad y empatía', 'Peso': 'SIN PESO', 'Precicion': 'NO CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '64', 'Item': 'Saludo', 'Peso': 'SIN PESO', 'Precicion': 'NO CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '65', 'Item': 'Despedida', 'Peso': 'SIN PESO', 'Precicion': 'NO CRÍTICO', 'Calificacion': 'cumple'}, {'IdItem': '66', 'Item': 'Tono de voz', 'Peso': 'SIN PESO', 'Precicion': 'NO CRÍTICO', 'Calificacion': 'cumple'}]}
#print(CalNotaMon(x))


def ExtDataDic(dic):
	#dic={'0': '52482028', '1': 1070968663, '2': 'GNP Centro', '3': 'CALIDAD', '4': 'JOAN CAMILO SERRANO CHAVEZ', '5': 'HFC', '6': 'MUESTRA', '7': '2022-09-23', '8': '1234', '9': '6547', '10': '26/09/2022', '11': 'Arreglo', '12': '1234', '13': 'B - DIRECCION Y/O DATOS ERRADOS', '14': '06:00 a 06:30', '15': 'pruebas observacion            ', '16': '100', '17': '0', '18': '0', '19': '0', '20': '{"datos":[{"IdItem":"37","Item":"Realiza acompañamiento al cliente evitando abandono de la llamada","Peso":"0","Precicion":"CRÍTICO","Calificacion":"cumple"},{"IdItem":"38","Item":"Realiza devolución de llamada en caso de caída","Peso":"0","Precicion":"CRÍTICO","Calificacion":"cumple"},{"IdItem":"39","Item":"Trata al cliente con respeto","Peso":"0","Precicion":"CRÍTICO","Calificacion":"cumple"},{"IdItem":"40","Item":"Uso correcto del canal","Peso":"0","Precicion":"CRÍTICO","Calificacion":"cumple"},{"IdItem":"41","Item":"Hace uso del token para reprogramar/cancelar visita","Peso":"0","Precicion":"CRÍTICO","Calificacion":"cumple"},{"IdItem":"42","Item":"Realiza contacto con el cliente","Peso":"0","Precicion":"CRÍTICO","Calificacion":"cumple"},{"IdItem":"43","Item":"Garantiza el cumplimiento de los compromisos adquiridos con el cliente","Peso":"0","Precicion":"CRÍTICO","Calificacion":"cumple"},{"IdItem":"44","Item":"Reprograma o cancela visita con autorización y contacto al cliente","Peso":"0","Precicion":"CRÍTICO","Calificacion":"cumple"},{"IdItem":"45","Item":"Programa visita según lo acordado con el cliente","Peso":"0","Precicion":"CRÍTICO","Calificacion":"cumple"},{"IdItem":"46","Item":"Garantiza permisos de administración","Peso":"0","Precicion":"CRÍTICO","Calificacion":"cumple"},{"IdItem":"47","Item":"Realiza preguntas que permitan dar solución al requerimiento del cliente","Peso":"0.3","Precicion":"NO CRÍTICO","Calificacion":"cumple"},{"IdItem":"48","Item":"Invita al cliente a usar el APP","Peso":"0.3","Precicion":"NO CRÍTICO","Calificacion":"cumple"},{"IdItem":"49","Item":"Cumple tiempos de gestión","Peso":"0.3","Precicion":"NO CRÍTICO","Calificacion":"cumple"},{"IdItem":"50","Item":"Cumple tiempos de seguimiento","Peso":"0.3","Precicion":"NO CRÍTICO","Calificacion":"cumple"},{"IdItem":"51","Item":"Garantiza marcar la razón en RR","Peso":"0.3","Precicion":"NO CRÍTICO","Calificacion":"cumple"},{"IdItem":"52","Item":"Registra notas de forma completa y correcta","Peso":"0.3","Precicion":"NO CRÍTICO","Calificacion":"cumple"},{"IdItem":"53","Item":"Confirma motivo de la creación de la OT/LLS","Peso":"0.3","Precicion":"NO CRÍTICO","Calificacion":"cumple"},{"IdItem":"54","Item":"Brinda información completa y correcta","Peso":"0.7","Precicion":"NO CRÍTICO","Calificacion":"cumple"},{"IdItem":"55","Item":"Escucha activa","Peso":"0.7","Precicion":"NO CRÍTICO","Calificacion":"cumple"},{"IdItem":"56","Item":"Tiempos de espera","Peso":"0.7","Precicion":"NO CRÍTICO","Calificacion":"cumple"},{"IdItem":"57","Item":"La solución atiende la necesidad del cliente","Peso":"0.7","Precicion":"NO CRÍTICO","Calificacion":"cumple"},{"IdItem":"58","Item":"Actualiza correo y teléfonos de contacto del cliente para el envío del token","Peso":"0.7","Precicion":"NO CRÍTICO","Calificacion":"cumple"},{"IdItem":"59","Item":"Uso adecuado de suspensión de eventos","Peso":"0.7","Precicion":"NO CRÍTICO","Calificacion":"cumple"},{"IdItem":"60","Item":"Confirma dirección del evento","Peso":"0.7","Precicion":"NO CRÍTICO","Calificacion":"cumple"},{"IdItem":"61","Item":"Genera solicitud para replanteamiento/ampliación de tap","Peso":"0.7","Precicion":"NO CRÍTICO","Calificacion":"cumple"},{"IdItem":"62","Item":"Realiza seguimiento a eventos razonados por R y H","Peso":"0.7","Precicion":"NO CRÍTICO","Calificacion":"cumple"},{"IdItem":"63","Item":"Amabilidad y empatía","Peso":"SIN PESO","Precicion":"NO CRÍTICO","Calificacion":"cumple"},{"IdItem":"64","Item":"Saludo","Peso":"SIN PESO","Precicion":"NO CRÍTICO","Calificacion":"cumple"},{"IdItem":"65","Item":"Despedida","Peso":"SIN PESO","Precicion":"NO CRÍTICO","Calificacion":"cumple"},{"IdItem":"66","Item":"Tono de voz","Peso":"SIN PESO","Precicion":"NO CRÍTICO","Calificacion":"cumple"}]}'}

	#print(dic)
	ArrayForm=[]
	for i,j in dic.items():
		if int(i)<20:
			ArrayForm.append(j)
	ArrayNotas=dic['20']
	DicNotas=json.loads(ArrayNotas).values()
	for i in DicNotas:
		ArrayNotas=i

	return [ArrayForm,ArrayNotas]


def CalNotaMonHp(valores):
	contitemcum=0
	contitemNocum=0	
	for i in valores.values():
		for j in i:
			if j['Calificacion']=="Cumple":
				contitemcum+=1
			elif j['Calificacion']=="No aplica":
				pass
			else:
				contitemNocum+=1
	nota=contitemcum/(contitemcum+contitemNocum)*100
	return contitemNocum,contitemcum,round(nota,1)

