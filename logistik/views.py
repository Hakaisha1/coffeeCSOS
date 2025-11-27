from django.shortcuts import render
from django.http import HttpResponse
from .models import Barang, Supplier
from .logistik import Barang as BarangOOP, Supplier as SupplierOOP
from .logistik import Gudang, LogistikManager
from datetime import date
from django.shortcuts import render, redirect


def proses_stok(request, id_barang):
    # 1. Ambil dari database
    barang_model = Barang.objects.get(id=id_barang)

    # 2. Convert ke object OOP
    barang_oop = BarangOOP(
        barang_model.nama,
        barang_model.stok,
        barang_model.harga,
        barang_model.kadaluarsa
    )

    # 3. Buat gudang OOP
    gudang = Gudang()
    gudang.tambah_barang(barang_oop)

    # 4. Buat manager dan jalankan logika OOP
    manager = LogistikManager(gudang)
    manager.beli_barang(
        supplier=SupplierOOP("Supplier Default", "08123xxx"),
        barang=barang_oop,
        jumlah=5,
        tanggal=str(date.today())
    )

    # 5. Kembalikan hasil ke database
    barang_model.stok = barang_oop.stok
    barang_model.save()

    return HttpResponse("Transaksi berhasil diproses.")


def daftar_barang(request):
    data = Barang.objects.all()
    return render(request, "logistik/nyoba.html", {"barang_list": data})

def tambah_barang(request):
    if request.method == "POST":
        nama = request.POST.get("nama")
        stok = request.POST.get("stok")
        harga = request.POST.get("harga")

        Barang.objects.create(
            nama=nama,
            stok=int(stok),
            harga=int(harga),
        )

        return redirect("daftar_barang")

    return render(request, "logistik/tambah_barang.html")