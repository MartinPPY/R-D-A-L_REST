from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class CompanyView(GenericAPIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        return Response({"company":"company"},status=status.HTTP_200_OK)
    
    
