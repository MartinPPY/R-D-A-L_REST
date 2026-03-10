from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

def login_and_get_tokens(username:str,password:str):
    
    user = authenticate(
        username=username,
        password=password
    )
    
    if user is None:
        raise AuthenticationFailed("Credenciales inválidas")

    # opcional, pero recomendado:
    if not user.is_active:
        raise AuthenticationFailed("Usuario inactivo")

    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    return {
        "user": user,
        "refresh": str(refresh),
        "access": str(access),
    }
   
def register_user(username:str,name:str,lastname:str,email:str,password:str):
    if User.objects.filter(username=username).exists():
        raise AuthenticationFailed("El nombre de usuario ya está en uso")
    
    if User.objects.filter(email=email).exists():
        raise AuthenticationFailed("El correo electrónico ya está en uso")
    
    user = User.objects.create_user(
        username=username,
        first_name=name,
        last_name=lastname,
        email=email,
        password=password,
    )
    
    user.save()
    
    return user

def reset_password(email:str,password:str):
    
    try:
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()        
        
    except User.DoesNotExist:        
        raise AuthenticationFailed("No se encontró un usuario con ese correo electrónico")
    

def get_groups_for_user(username:str):
    try:
        user = User.objects.get(username=username)
        return user.groups.all()
    except User.DoesNotExist:
        raise AuthenticationFailed("No se encontró un usuario con ese nombre de usuario")
    