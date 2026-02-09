from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import *
from .services import *

# Create your views here.
class LoginView(GenericAPIView):
    
    permission_classes = [AllowAny] # Permitir acceso a esta funcion sin autenticación
    authentication_classes = []  
    serializer_class = LoginSerializer
    
    def post(self,*args,**kwargs):
        serializer_class = self.get_serializer(data=self.request.data)        
        
        serializer_class.is_valid(raise_exception=True)
        
        tokens = login_and_get_tokens(
            username=serializer_class.validated_data["username"],
            password=serializer_class.validated_data["password"],
        )    
        
        response = Response({"message":"OK"},status=status.HTTP_200_OK)
        
        response.set_cookie(
            key="access_token",
            value=tokens["access"],
            httponly=True,
            secure=True,          
            samesite="Lax", 
        )
        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh"],
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        return response

class RegisterView(GenericAPIView):
    
    permission_classes = [AllowAny] # Permitir acceso a esta funcion sin autenticación
    authentication_classes = []      
    serializer_class = RegisterSerializer
    
    def post(self,*args,**kwargs):
        
        serializer_class = self.get_serializer(data=self.request.data)
        
        serializer_class.is_valid(raise_exception=True)
        
        register_user(
            username=serializer_class.validated_data["username"],
            name=serializer_class.validated_data["name"],
            lastname=serializer_class.validated_data["lastname"],
            email=serializer_class.validated_data["email"],
            password=serializer_class.validated_data["password"],
            is_admin=serializer_class.validated_data["is_admin"],
        )
        
        return Response({"message":"Usuario creado correctamente!"},status=status.HTTP_201_CREATED)


class LogoutView(GenericAPIView):    
    
    def post(self,request):
        
        response = Response({"message":"Logged out successfully!"},status=status.HTTP_200_OK)
        
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        
        return response

class ForgotPasswordView(GenericAPIView):
    
    permission_classes = [AllowAny] # Permitir acceso a esta funcion sin autenticación
    authentication_classes = []
    serializer_class = ForgotPasswordSerializer
    
    def post(self,*args,**kwargs):
        
        serializer_class = self.get_serializer(data=self.request.data)
        
        serializer_class.is_valid(raise_exception=True)
        
        reset_password(
            email=serializer_class.validated_data["email"],
            password=serializer_class.validated_data["password"],
        )
        
        return Response({"message":"Password reset email sent!"},status=status.HTTP_200_OK)

class GetPermissions(GenericAPIView):
    
    permision_classes = [IsAuthenticated]
    
    def get(self,request,*args,**kwargs):
        
        username = request.user
        permisos  = get_groups_for_user(username)        
        return Response(
            {"permisos":permisos.values_list(flat=False)},status=status.HTTP_200_OK
        )
    
    