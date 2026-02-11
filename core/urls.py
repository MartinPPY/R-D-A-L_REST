from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register(r'actividad',ActivityViewSet,basename="actividad")




urlpatterns = [    
    path("area",AreaView.as_view(),name="area"),    
    path("",include(router.urls)),
    path("resumen",get_resumen_usuario,name="resumen")
]
