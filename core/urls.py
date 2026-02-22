from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register(r'actividad',ActivityViewSet,basename="actividad")
router.register(r'orden-compra',OrdenPagoViewSet,basename="orden-compra")
router.register(r'area',AreaViewSet,basename="area")




urlpatterns = [    
    path("",include(router.urls)),
    path("resumen",ResumenUsuarioView.as_view(),name="resumen"),
    path("resumen-admin",ResumenMensualAdmin.as_view(),name="resumen-admin"),
    path("resumen-pago",ResumenOrdenCompra.as_view(),name="resumen-pago"),
]
