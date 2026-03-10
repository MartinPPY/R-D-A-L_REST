from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
# Create your models here.

class ActivityQuerySet(models.QuerySet):
    def for_user(self, user):
        """Filtra actividades según el rol del usuario."""
        if user.groups.filter(name="usuario").exists():
            return self.filter(user=user)
        return self.all()

    def current_month(self):
        """Filtra actividades del mes actual."""
        hoy = date.today()
        return self.filter(fecha__year=hoy.year, fecha__month=hoy.month)

class ActivityManager(models.Manager):
    def get_queryset(self):
        return ActivityQuerySet(self.model, using=self._db)

    def for_user_request(self, user):
        """Lógica de filtrado combinada para las vistas."""
        qs = self.get_queryset().for_user(user)
        # Si es admin (no es 'usuario'), aplicamos filtro de mes por defecto
        if not user.groups.filter(name="usuario").exists():
            return qs.current_month()
        return qs

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
    
    objects = ActivityManager()

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



