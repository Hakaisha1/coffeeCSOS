from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum
from datetime import date

from .models import Barang, Supplier
from .logistik import Barang as BarangOOP, Supplier as SupplierOOP
from .logistik import Gudang, LogistikManager

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

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
        stok_minimum = int(request.POST.get("stok_minimum", 10))
        kadaluarsa = request.POST.get("kadaluarsa")
        harga = request.POST.get("harga")
        
        # Validasi kadaluarsa: harus kosong atau format tanggal yang benar
        if kadaluarsa and len(kadaluarsa.strip()) > 0:
            # Cek apakah format valid (minimal ada dash untuk YYYY-MM-DD)
            if '-' not in kadaluarsa:
                kadaluarsa = None
        else:
            kadaluarsa = None

        Barang.objects.create(
            nama=nama,
            stok=stok,
            stok_minimum=stok_minimum,
            harga=harga,
            kadaluarsa=kadaluarsa,
        )

        return redirect("daftar_barang")

    return render(request, "logistik/tambah_barang.html")


def api_barang(request):
    data = list(Barang.objects.values())
    return JsonResponse({"barang": data})

def api_dashboard(request):
    total_barang = Barang.objects.count()
    total_stok = sum(b.stok for b in Barang.objects.all())
    barang_kosong = Barang.objects.filter(stok=0).count()

    return JsonResponse({
        "total_barang": total_barang,
        "total_stok": total_stok,
        "barang_kosong": barang_kosong
    })


def supplier(request):
    supplier_list = Supplier.objects.all()
    return render(request, "logistik/supllier.html", {
        "supplier_list": supplier_list
    })

def api_supplier(request):
    data = list(Supplier.objects.values())
    return JsonResponse({"supplier": data})

def edit_barang(request, id_barang):
    barang = get_object_or_404(Barang, id=id_barang)

    if request.method == "POST":
        barang.nama = request.POST.get("nama")
        barang.stok = request.POST.get("stok")
        barang.harga = request.POST.get("harga")
        barang.save()

        return redirect("daftar_barang")

    return render(request, "logistik/edit_barang.html", {"barang": barang})
