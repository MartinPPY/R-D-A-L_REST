from .models import *
from django.contrib.auth.models import User 
from datetime import date
from django.db.models import Prefetch, Exists, OuterRef

TARIFA = 2500

def get_areas():
    areas = Area.objects.all()
    return areas

#Resumen del mes por alumno
def get_resumen(username):
    hoy = date.today()
    total_cantidad_horas = 0
    total_dinero_acumulado = 0
    total_horas_aprobadas = 0
    
    #obtener el total de horas por mes
    user = User.objects.get(username=username)
    actividades_resumen = Activity.objects.filter(user=user,fecha__month=hoy.month,fecha__year=hoy.year)

    for actividad in actividades_resumen:        
        
        total_cantidad_horas += actividad.diferencia_horas()

        if actividad.aprobado:
            total_horas_aprobadas +=1            
            total_dinero_acumulado += actividad.diferencia_horas() * TARIFA
    
    
    orden_compra = OrdenCompra.objects.filter(user=user, fecha__month=date.today().month, fecha__year=date.today().year).first()


    resumen_mensual = {
        "horas_acumuladas":total_cantidad_horas,
        "total_acumulado":total_dinero_acumulado,
        "horas_aprobadas":total_horas_aprobadas,
        "orden_compra":orden_compra.pk if orden_compra else None
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
    ).annotate(
        tiene_orden_compra=Exists(
            OrdenCompra.objects.filter(
                user=OuterRef('pk'),
                fecha__month=hoy.month,
                fecha__year=hoy.year
            )
        )
    ).prefetch_related(
        Prefetch(
            'activity_set',
            queryset=Activity.objects.filter(
                fecha__year=hoy.year,
                fecha__month=hoy.month,
                aprobado=True
            )
        )
    )

    for usuario in usuarios:

        if usuario.tiene_orden_compra:
            continue
        
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

# SERVICIOS DE VALIDACIÓN
def check_activity_overlap(user, fecha, hora_inicio, hora_fin, exclude_id=None):
    """
    Verifica si una actividad se superpone con otras del mismo usuario en el mismo mes.
    Retorna True si hay superposición, False en caso contrario.
    """
    from .models import Activity
    
    # Obtenemos las actividades del mes para ese usuario
    qs = Activity.objects.filter(
        user=user,
        fecha__year=fecha.year,
        fecha__month=fecha.month,
        fecha=fecha
    )
    
    if exclude_id:
        qs = qs.exclude(id=exclude_id)

    for actividad in qs:
        # Lógica de superposición: (Inicio1 < Fin2) AND (Fin1 > Inicio2)
        if hora_inicio < actividad.hora_fin and hora_fin > actividad.hora_inicio:
            return True
            
    return False
        


    

    


