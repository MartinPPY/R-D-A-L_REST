from django.urls import path
from .views import *


urlpatterns = [
    
    path("area",AreaView.as_view(),name="area")
    
]
