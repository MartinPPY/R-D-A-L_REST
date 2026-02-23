from rest_framework.generics import GenericAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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
        user = self.request.user
        hoy = date.today()

        if user.groups.filter(name="usuario").exists():
            return Activity.objects.filter(user=user)
        
        
        
        return Activity.objects.filter(
            fecha__year=hoy.year,
            fecha__month=hoy.month
        )

    def perform_create(self, serializer):
        
        serializer.save(user=self.request.user)


class ResumenUsuarioView(GenericAPIView):

    serializer_class = EmptySerializer

    def get(self,request,*args,**kwargs):

        username = request.user.username
        resumen = get_resumen(username=username)
        return Response(
            resumen,
            status=status.HTTP_200_OK
        )

class ResumenMensualAdmin(GenericAPIView):

    serializer_class = EmptySerializer

    def get(self,request,*args,**kwargs):

        resumen = get_resumen_admin()

        return Response(
            resumen,
            status=status.HTTP_200_OK
        )

class ResumenOrdenCompra(GenericAPIView):
    
    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated]

    def get(self,request,*args,**kwargs):

        resumen = get_orden_compra()

        return Response(resumen,status=status.HTTP_200_OK)


class OrdenPagoViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = OrdenPagoSerializer
    queryset = OrdenCompra.objects.all()
    



    

        
    
    
