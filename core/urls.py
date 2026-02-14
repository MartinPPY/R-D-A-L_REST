from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register(r'actividad',ActivityViewSet,basename="actividad")
router.register(r'orden-compra',OrdenPagoViewSet,basename="orden-compra")




urlpatterns = [    
    path("area",AreaView.as_view(),name="area"),    
    path("",include(router.urls)),
    path("resumen",ResumenUsuarioView.as_view(),name="resumen"),
    path("resumen-admin",ResumenMensualAdmin.as_view(),name="resumen-admin"),
    path("resumen-pago",ResumenOrdenCompra.as_view(),name="resumen-pago"),
]
