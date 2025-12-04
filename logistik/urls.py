from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_logistik, name="dashboard_logistik"),
    path("barang/", views.daftar_barang, name="daftar_barang"),
    path("tambah/", views.tambah_barang, name="tambah_barang"),
]

