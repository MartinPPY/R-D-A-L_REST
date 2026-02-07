from django.urls import path
from .views import *


urlpatterns = [
    
    path('company',CompanyView.as_view(),name='company')
    
]
