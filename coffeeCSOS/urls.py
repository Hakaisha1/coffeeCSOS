"""
URL configuration for coffeeCSOS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        'message': 'CoffeeCSOS API',
        'endpoints': {
            'pegawai': '/pegawai/api/pegawai/',
            'barista': '/pegawai/api/barista/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # CONTOH LENGKAP: Include report URLs
    # Semua URL dari report.urls akan diakses dengan prefix 'reports/'
    # Contoh: /reports/, /reports/employee/, /reports/api/employee/
    path('reports/', include('report.urls')),
    
    # TODO (OPTIONAL): Tambahkan URL patterns untuk app lain jika diperlukan
    # HINT untuk customer app:
    # path('customer/', include('customer.urls')),
    
    # HINT untuk pegawai app:
    # path('pegawai/', include('pegawai.urls')),
    path('pegawai/', include('pegawai.urls')),
    path('logistik/', include('logistik.urls')),

]
