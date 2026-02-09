from django.db import models
# Create your models here.

class Area(models.Model):
    
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name


class Activity(models.Model):
    
    name = models.CharField(max_length=255)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    aprobado = models.BooleanField(default=False)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
