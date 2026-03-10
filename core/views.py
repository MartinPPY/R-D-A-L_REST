from rest_framework.generics import GenericAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from datetime import date

from .serializers import *
from .services import *
from .models import *

class AreaViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    
    
    

class ActivityViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_queryset(self):
        # MEJORA: La lógica de filtrado ahora vive en el Manager del Modelo
        return Activity.objects.for_user_request(self.request.user)

    def perform_create(self, serializer):
        # Simplificado: El user ya se pasa en el serializer.save si es necesario o aquí
        serializer.save(user=self.request.user)


class ResumenUsuarioView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @extend_schema(
        responses={200: ResumenUsuarioResponseSerializer},
        description="Obtiene un resumen de horas y montos acumulados del usuario autenticado."
    )
    def get(self,request,*args,**kwargs):

        username = request.user.username
        resumen = get_resumen(username=username)
        return Response(
            resumen,
            status=status.HTTP_200_OK
        )

class ResumenMensualAdmin(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @extend_schema(
        responses={200: ResumenMensualAdminResponseSerializer},
        description="Resumen mensual general para administradores (usuarios, horas, órdenes)."
    )
    def get(self,request,*args,**kwargs):

        resumen = get_resumen_admin()

        return Response(
            resumen,
            status=status.HTTP_200_OK
        )

class ResumenOrdenCompra(GenericAPIView):
    
    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: ResumenOrdenCompraItemSerializer(many=True)},
        description="Obtiene la lista de pagos pendientes (usuarios sin orden de compra este mes)."
    )
    def get(self,request,*args,**kwargs):

        resumen = get_orden_compra()

        return Response(resumen,status=status.HTTP_200_OK)


class OrdenPagoViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = OrdenPagoSerializer
    queryset = OrdenCompra.objects.all()
    



    

        
    
    
