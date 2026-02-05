from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny #permite que el endpoint sea accesible sin autenticación
from rest_framework import status
from .models import *

# Create your views here.
class LocationView(APIView):
    
    permission_classes = [AllowAny] # Permitir acceso a esta funcion sin autenticación
    authentication_classes = []  
    
    regiones = Region.objects.all()
    
    def get(self, request):
        regiones_data = [{"id": region.id, "name": region.name} for region in self.regiones]
        return Response({"regiones": regiones_data},status=status.HTTP_200_OK)
