from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .services import *

class AreaView(GenericAPIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self,request,*args,**kwargs):
        areas = get_areas()
        return Response(
            {"areas":list(areas.values())},
            status=status.HTTP_200_OK
        )
        
    
    
