from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
# Create your models here.

class Area(models.Model):
    
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name


class Activity(models.Model):
    
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    aprobado = models.BooleanField(default=False)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username + " " + self.area.name 
    
    def diferencia_horas(self):
        inicio = datetime.combine(datetime.today(), self.hora_inicio)
        fin = datetime.combine(datetime.today(), self.hora_fin)

        # Por si cruza medianoche
        if fin < inicio:
            fin += timedelta(days=1)

        horas = (fin - inicio).total_seconds() / 3600
        return round(horas)

class OrdenCompra(models.Model):

    fecha = models.DateField()
    monto = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.monto) + " " + self.user.username



