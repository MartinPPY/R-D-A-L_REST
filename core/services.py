from .models import *

def get_areas():
    areas = Area.objects.all()
    return areas