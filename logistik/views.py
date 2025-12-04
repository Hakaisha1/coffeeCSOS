from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum
from datetime import date

from .models import Barang, Supplier
from .logistik import Barang as BarangOOP, Supplier as SupplierOOP
from .logistik import Gudang, LogistikManager



# =============================
# PROSES STOK (OOP LOGIC)
# ============================
from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.decorators import role_required


@login_required
@role_required(['INVENTORY_MANAGER','GENERAL_MANAGER'])
def proses_stok(request, id_barang):
    barang_model = Barang.objects.get(id=id_barang)

    # Convert ke OOP
    barang_oop = BarangOOP(
        barang_model.nama,
        barang_model.stok,
        barang_model.harga,
        barang_model.kadaluarsa
    )

    gudang = Gudang()
    gudang.tambah_barang(barang_oop)

    manager = LogistikManager(gudang)
    manager.beli_barang(
        supplier=SupplierOOP("Supplier Default", "08123xxx"),
        barang=barang_oop,
        jumlah=5,
        tanggal=str(date.today())
    )

    # Simpan perubahan ke DB
    barang_model.stok = barang_oop.stok
    barang_model.save()

    return HttpResponse("Transaksi berhasil diproses.")



# =============================
# DASHBOARD LOGISTIK
# =============================
def dashboard_logistik(request):
    total_barang = Barang.objects.count()
    total_stok = Barang.objects.aggregate(total=Sum('stok'))['total'] or 0
    barang_hampir_habis = Barang.objects.filter(stok__lte=5).count()

    barang_list = Barang.objects.all()[:5]  # contoh menampilkan 5 barang teratas

    context = {
        "total_barang": total_barang,
        "total_stok": total_stok,
        "barang_hampir_habis": barang_hampir_habis,
        "barang_list": barang_list,
    }

    return render(request, "logistik/dashboardlogis.html", context)


# =============================
# DAFTAR BARANG
# =============================
def daftar_barang(request):
    barang = Barang.objects.all()

    context = {
        "barang_list": barang,
    }
    return render(request, "logistik/daftar_barang.html", context)


# =============================
# TAMBAH BARANG
# =============================

@login_required
@role_required(['INVENTORY_MANAGER','GENERAL_MANAGER'])
def daftar_barang(request):
    data = Barang.objects.all()
    return render(request, "logistik/daftar_barang.html", {"barang_list": data})

@login_required
@role_required(['INVENTORY_MANAGER','GENERAL_MANAGER'])

def tambah_barang(request):
    if request.method == "POST":
        nama = request.POST.get("nama")
        stok = int(request.POST.get("stok"))
        harga = int(request.POST.get("harga"))

        Barang.objects.create(
            nama=nama,
            stok=stok,
            harga=harga,
        )

        return redirect("daftar_barang")

    return render(request, "logistik/tambah_barang.html")
