from .models import *
from django.contrib.auth.models import User 

def get_areas():
    areas = Area.objects.all()
    return areas

#Resumen del mes por alumno
def get_resumen(username):
    TARIFA = 2500
    total_cantidad_horas = 0
    total_dinero_acumulado = 0
    total_horas_aprobadas = 0
    
    #obtener el total de horas por mes
    user = User.objects.get(username=username)
    actividades_resumen = Activity.objects.filter(user=user)
    for actividad in actividades_resumen:        
        
        total_cantidad_horas += actividad.diferencia_horas()

        if actividad.aprobado:
            total_horas_aprobadas +=1            
            total_dinero_acumulado += actividad.diferencia_horas() * TARIFA
    


    resumen_mensual = {
        "horas_acumuladas":total_cantidad_horas,
        "total_acumulado":total_dinero_acumulado,
        "horas_aprobadas":total_horas_aprobadas
    }

    return resumen_mensual