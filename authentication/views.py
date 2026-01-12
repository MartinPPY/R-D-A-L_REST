from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

#traemos los modelos de core
from ..core.models import Company

# Create your views here.
class LoginView(APIView):
    
    permission_classes = [] # Permitir acceso a esta funcion sin autenticación
    
    def post(self,request):
                
        user = authenticate(
            username = request.data["username"],
            password = request.data["password"]
        )
        
        if not user:
            return Response(
                {"message":"Credenciales invalidas"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        refresh = RefreshToken.for_user(user)
        
        response = Response(
            {"message":"OK"},
            status=status.HTTP_200_OK
        )
        
        response.set_cookie(
            key="access_token",
            value=str(refresh.access_token),
            httponly=True,
            secure=True,
            samesite="Lax"
        )
        
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        return response
        
class RegisterView(APIView):
    
    def post(self,request):
        
        company = Company()
        
        company.name = "    "
            
        return ""
        
        
