from rest_framework import serializers


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
class RegisterSerializer(serializers.Serializer):
    
    username = serializers.CharField()
    name = serializers.CharField()
    lastname = serializers.CharField()    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
class ForgotPasswordSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class EmptySerializer(serializers.Serializer):
    pass

# SERIALIZERS PARA DOCUMENTACIÓN SWAGGER
class MessageResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

class GetPermissionsResponseSerializer(serializers.Serializer):
    permisos = serializers.ListField(child=serializers.ListField())

class CheckAuthResponseSerializer(serializers.Serializer):
    user = serializers.CharField()
