from .models import *
from django.contrib.auth.models import User


def get_company_by_user(username:str):
    
    try:
        
        user = User.objects.get(username=username)
        company = user.company
        
        if not company:
            raise Exception("Company not found")
        
        return company
    
    except:
        raise Exception("User not found")