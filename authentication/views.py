from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from drf_spectacular.utils import extend_schema
from .serializers import *
from .services import *

# Create your views here.
class LoginView(GenericAPIView):
    
    permission_classes = [AllowAny] # Permitir acceso a esta funcion sin autenticación
    authentication_classes = []  
    serializer_class = LoginSerializer
    
    @extend_schema(
        responses={200: MessageResponseSerializer},
        description="Autentica al usuario y establece cookies 'access_token' y 'refresh_token'."
    )
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
    
    @extend_schema(
        responses={201: MessageResponseSerializer},
        description="Registra un nuevo usuario en el sistema."
    )
    def post(self,*args,**kwargs):
        
        serializer_class = self.get_serializer(data=self.request.data)
        
        serializer_class.is_valid(raise_exception=True)
        
        register_user(
            username=serializer_class.validated_data["username"],
            name=serializer_class.validated_data["name"],
            lastname=serializer_class.validated_data["lastname"],
            email=serializer_class.validated_data["email"],
            password=serializer_class.validated_data["password"],
        )
        
        return Response({"message":"Usuario creado correctamente!"},status=status.HTTP_201_CREATED)


class LogoutView(GenericAPIView):

    serializer_class = EmptySerializer
    
    @extend_schema(
        responses={200: MessageResponseSerializer},
        description="Cierra la sesión eliminando las cookies de autenticación."
    )
    def post(self,request):
        
        response = Response({"message":"Logged out successfully!"},status=status.HTTP_200_OK)
        
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.delete_cookie("csrftoken")
        response.delete_cookie("sessionid")
        
        return response

class ForgotPasswordView(GenericAPIView):
    
    permission_classes = [AllowAny] # Permitir acceso a esta funcion sin autenticación
    authentication_classes = []
    serializer_class = ForgotPasswordSerializer
    
    """
    @extend_schema(
        responses={200: MessageResponseSerializer},
        description="Resetea la contraseña del usuario (Flujo desactivado por seguridad)."
    )
    def post(self,*args,**kwargs):
        return Response({"message":"Flujo de recuperación desactivado por seguridad."},status=status.HTTP_403_FORBIDDEN)
    """

class GetPermissions(GenericAPIView):
    
    # Corregido: permission_classes (para correcta documentación y seguridad)
    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer
    
    @extend_schema(
        responses={200: GetPermissionsResponseSerializer},
        description="Retorna la lista de permisos (grupos) del usuario autenticado."
    )
    def get(self,request,*args,**kwargs):
        
        username = request.user
        permisos  = get_groups_for_user(username)        
        return Response(
            {"permisos":permisos.values_list(flat=False)},status=status.HTTP_200_OK
        )
    

class RefreshTokenView(GenericAPIView):

    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = EmptySerializer

    @extend_schema(
        responses={200: MessageResponseSerializer},
        description="Refresca el token de acceso usando la cookie 'refresh_token'."
    )
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            raise AuthenticationFailed("Refresh token no encontrado")

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except Exception:
            raise AuthenticationFailed("Refresh token inválido o expirado")

        response = Response({"message": "OK"}, status=status.HTTP_200_OK)

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        return response

class CheckAuthView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @extend_schema(
        responses={200: CheckAuthResponseSerializer},
        description="Verifica si el usuario está autenticado y retorna su username."
    )
    def get(self,request,*args,**kwargs):

        username = request.user.username
        response_body = {
            "user":username
        }
        return Response(response_body,status=status.HTTP_200_OK)

    