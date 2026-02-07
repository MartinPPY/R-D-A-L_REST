from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .services import *

class CompanyView(GenericAPIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        
        company = get_company_by_user(username=request.user.username)
        return Response({"company":company},status=status.HTTP_200_OK)
    
    
