from django.urls import path
from . import views

urlpatterns = [
    path("proses/<int:id_barang>/", views.proses_stok, name="proses_stok"),
    path("", views.daftar_barang, name="daftar_barang"),
    path("proses/<int:id_barang>/", views.proses_stok, name="proses_stok"),
    path("", views.daftar_barang, name="daftar_barang"),
    path("tambah/", views.tambah_barang, name="tambah_barang"),
]
