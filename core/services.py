from .models import *
from django.contrib.auth.models import User 
from datetime import date
from django.db.models import Prefetch

TARIFA = 2500

def get_areas():
    areas = Area.objects.all()
    return areas

#Resumen del mes por alumno
def get_resumen(username):
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

def get_resumen_admin():

    total_cantidad_horas = 0

    cantidad_usuarios = User.objects.filter(
        groups__name="usuario"
    ).count()    

    hoy = date.today()

    actividades = Activity.objects.filter(
        fecha__year=hoy.year,
        fecha__month=hoy.month
    )

    cantidad_orden_compra_mes = OrdenCompra.objects.filter(
        fecha__year=hoy.year,
        fecha__month=hoy.month
    ).count()

    for actividad in actividades:
        total_cantidad_horas += actividad.diferencia_horas()
    
    resumen_mensual = {
        "usuarios":cantidad_usuarios,
        "cantidad_horas":total_cantidad_horas,
        "cantidad_orden_compra":cantidad_orden_compra_mes
    }

    return resumen_mensual

def get_orden_compra():

    hoy = date.today()
    lista_pagos = []

    usuarios = User.objects.filter(
        groups__name="usuario"
    ).prefetch_related(
        Prefetch(
            'activity_set',
            queryset=Activity.objects.filter(
                fecha__year=hoy.year,
                fecha__month=hoy.month
            )
        )
    )

    for usuario in usuarios:
        
        total = sum(
            act.diferencia_horas() * TARIFA
            for act in usuario.activity_set.all()
        )

        if total == 0:
            continue

        resumen_usuario = {
            "user_id":usuario.pk,
            "usuario":usuario.get_full_name(),
            "monto_acumulado":total,
            "orden_compra":None         
        }

        lista_pagos.append(resumen_usuario)
    
    return lista_pagos
        


    

    


