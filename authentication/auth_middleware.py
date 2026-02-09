from rest_framework_simplejwt.authentication import JWTAuthentication

# middleware para validar el token

class CookieJWTAuthentication(JWTAuthentication):
    
    def authenticate(self, request):
        raw_token = request.COOKIES.get("access_token")
        if raw_token is None:
            return None
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
    
    
    def authenticate_header(self, request):
        # Evita que SimpleJWT intente usar AUTH_HEADER_TYPES[0]
        return ""