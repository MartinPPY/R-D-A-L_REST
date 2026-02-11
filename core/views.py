from rest_framework.generics import GenericAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse

from .serializers import *
from .services import *
from .models import *

class AreaView(GenericAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer
    
    def get(self,request,*args,**kwargs):
        areas = get_areas()
        return Response(
            {"areas":list(areas.values())},
            status=status.HTTP_200_OK
        )

class ActivityViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="usuario").exists():
            return Activity.objects.filter(user=user)
        
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_resumen_usuario(request):

    username = request.user.username
    resumen = get_resumen(username=username)
    
    return JsonResponse(resumen)





    

        
    
    
