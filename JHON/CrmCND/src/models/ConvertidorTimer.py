import datetime
import math





class Trazador:
	@classmethod
	def mixhora(self,horas_float):
	    #time_seconds = math.floor(horas_float * 60 * 60)
	    #time_formatted = datetime.datetime.utcfromtimestamp(time_seconds).strftime('%H:%M:%S')
	    time_formatted = datetime.timedelta(seconds=horas_float)
	    return time_formatted

	@classmethod
	def convertir_segundos_a_hora(self,segundos):
		# Crear un objeto timedelta con los segundos proporcionados
		delta = datetime.timedelta(seconds=segundos)

		# Crear un objeto datetime con la diferencia del tiempo actual y el timedelta
		tiempo_actual = datetime.datetime.now()
		hora = tiempo_actual + delta

		# Formatear y devolver la representación de la hora
		hora_formateada = hora.strftime("%H:%M:%S")
		return hora_formateada




