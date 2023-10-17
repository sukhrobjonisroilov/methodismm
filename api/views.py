from django.shortcuts import render
from methodism import METHODISM
# Create your views here.
from .models import AuthToken
from .service.views import ishlash
from api import service


class Methodism(METHODISM):
    file = service
    not_auth_methods = ['ishlash', 'auth.two', 'login','register']
    token_class = AuthToken

    token_key = "DarsBearerToken"
    auth_headers = 'DarsAuth'
