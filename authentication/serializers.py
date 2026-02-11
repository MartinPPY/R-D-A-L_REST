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
    is_admin = serializers.BooleanField(default=False)
    
class ForgotPasswordSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class EmptySerializer(serializers.Serializer):
    pass
