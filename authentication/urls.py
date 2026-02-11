from django.urls import path
from .views import *

urlpatterns = [
    path('login',LoginView.as_view(),name="login"),
    path('logout',LogoutView.as_view(),name="logout"),
    path('register',RegisterView.as_view(),name="register"),
    path('forgot-password',ForgotPasswordView.as_view(),name="forgot-password"),
    path('permissions',GetPermissions.as_view(),name="permissions"),
    path('refresh',RefreshTokenView.as_view(),name="refresh")
]