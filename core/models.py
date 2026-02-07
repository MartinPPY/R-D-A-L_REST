from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    
    name = models.CharField(max_length=255)
    
    #relacion 1 a 1 with User
    user = models.OneToOneField(User, on_delete=models.CASCADE)        
    
    
    def __str__(self):
        return self.name

class Area(models.Model):
    
    name = models.CharField(max_length=255)
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class Activity(models.Model):
    
    name = models.CharField(max_length=255)
    
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
