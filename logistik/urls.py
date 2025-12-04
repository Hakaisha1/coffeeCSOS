from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_logistik, name="dashboard_logistik"),

    # API AJAX
    path("api/dashboard/", views.api_dashboard, name="api_dashboard"),
    path("api/barang/", views.api_barang, name="api_barang"),

    # Halaman barang
    path("barang/", views.daftar_barang, name="daftar_barang"),
    path("tambah/", views.tambah_barang, name="tambah_barang"),

    path("supplier/", views.supplier, name="supplier"),
    # path("supplier/tambah/", views.tambah_supplier, name="tambah_supplier"),
    # path("supplier/edit/<int:id>/", views.edit_supplier, name="edit_supplier"),

    # API (untuk AJAX)
    path("api/supplier/", views.api_supplier, name="api_supplier"),
    path("edit/<int:id_barang>/", views.edit_barang, name="edit_barang"),


]
