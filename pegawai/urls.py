from django.urls import path
from . import views

app_name = 'pegawai'

urlpatterns = [
    # Semua data pegawai
    path('', views.index, name='pegawai_index'),
    
    # Data pegawai berdasarkan ID
    path('api/pegawai/<str:id_pegawai>/', views.detail_pegawai, name='detail_pegawai'),
    path('api/pegawai/create/', views.create_pegawai, name='create_pegawai'),
    path('api/pegawai/update/<str:id_pegawai>/', views.update_pegawai, name='update_pegawai'),
    path('api/pegawai/delete/<str:id_pegawai>/', views.delete_pegawai, name='delete_pegawai'),
    path('api/barista/', views.list_barista, name='list_barista'),
]