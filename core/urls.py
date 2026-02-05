from django.urls import path
from .views import LocationView

urlpatterns = [
    path('location/regiones',LocationView.as_view(),name="location/regiones")
]