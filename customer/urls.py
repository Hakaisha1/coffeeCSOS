from django.urls import path
from . import views
from django.views.generic import RedirectView

app_name = 'customer'  

urlpatterns = [
    path('', RedirectView.as_view(url='menu/', permanent=False)),  
    path('menu/', views.menu_view, name='menu'),
    path('manajemen-member/', views.manajemen_member, name='manajemen_member'),
    path('tambah-member-ajax/', views.tambah_member_ajax, name='tambah_member_ajax'),
    path('tambah-menu/', views.tambah_menu_view, name='tambah_menu'),
    path('riwayat/', views.riwayat_view, name='riwayat'),
]
