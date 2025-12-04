from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
# Create your views here.

def login_view(request):
    pass

def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard_view(request):
    if request.user.role =='GENERAL_MANAGER':
        pass
    elif request.user.role == 'INVENTORY_MANAGER':
        pass
    else:
        pass

