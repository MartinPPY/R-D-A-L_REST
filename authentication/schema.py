from drf_spectacular.extensions import OpenApiAuthenticationExtension

class CookieJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    # IMPORTANTE: string path, no la clase directa
    target_class = 'authentication.auth_middleware.CookieJWTAuthentication'
    name = 'CookieJWTAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'cookie',
            'name': 'access_token',
        }
