from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=100)

class Commune(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

class Company(models.Model):
    
    name = models.CharField(max_length=100)
    run = models.CharField(max_length=20, unique=True)
    comuna = models.ForeignKey(Commune, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    