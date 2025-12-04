from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_view, name='menu'),                 # Halaman Pesanan      # Top-up Saldo
    path('riwayat/', views.riwayat_view, name='customer_riwayat'), # Riwayat Transaksi
    path('tambah-menu/', views.tambah_menu_view, name='tambah_menu'),
]
