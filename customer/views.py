from django.db import transaction
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Customer, MenuItem, Pesanan, PesananDetail, Riwayat, Member, MenuItemBahan

# Halaman Menu 
def menu_view(request):
    menu = MenuItem.objects.all()
    cart = request.session.get("cart", [])
    error = None
    kembalian = request.session.pop("kembalian", None)
    diskon = 0
    total_bayar = sum(item["total"] for item in cart)
    total_bayar_diskon = total_bayar
    member_obj = None
    nama_input = ""

    if request.method == "POST":
        # ADD ITEM
        if "add_item" in request.POST:
            item_id = int(request.POST.get("item_id"))
            menu_item = MenuItem.objects.get(id=item_id)
            for item in cart:
                if item["id"] == item_id:
                    item["qty"] += 1
                    item["total"] = item["qty"] * item["harga"]
                    break
            else:
                cart.append({
                    "id": menu_item.id,
                    "nama": menu_item.nama,
                    "harga": int(menu_item.harga),
                    "qty": 1,
                    "total": int(menu_item.harga),
                })
            request.session["cart"] = cart
            messages.success(request, f"{menu_item.nama} ditambahkan ke keranjang.")
            return redirect("customer:menu")

        # HAPUS ITEM
        if "hapus_item" in request.POST:
            item_id = int(request.POST.get("item_id"))
            cart = [c for c in cart if c["id"] != item_id]
            request.session["cart"] = cart
            messages.success(request, "Item dihapus dari keranjang.")
            return redirect("customer:menu")

        # CEK DISKON
        if "cek_diskon" in request.POST:
            nama_input = request.POST.get("nama", "").strip()
            if nama_input:
                member_obj = Member.objects.filter(nama__iexact=nama_input).first()
                if member_obj:
                    diskon = int(total_bayar * 0.05)
                    total_bayar_diskon = total_bayar - diskon
            else:
                error = "Nama customer wajib diisi untuk cek diskon."

        # BAYAR
        if "checkout" in request.POST:
            nama_input = request.POST.get("nama", "").strip()
            bayar_input = request.POST.get("bayar", "0").replace(",", "")
            if not bayar_input.isdigit():
                error = "Uang bayar harus angka."
                bayar = 0
            else:
                bayar = int(bayar_input)

            total_bayar = sum(item["total"] for item in cart)
            member_obj = Member.objects.filter(nama__iexact=nama_input).first()
            diskon = int(total_bayar * 0.05) if member_obj else 0
            total_bayar_diskon = total_bayar - diskon

            if not nama_input:
                error = "Nama customer wajib diisi."
            elif not cart:
                error = "Keranjang masih kosong."
            elif bayar < total_bayar_diskon:
                error = f"Uang kurang. Total Rp{total_bayar_diskon:,}"
            else:
                try:
                    with transaction.atomic():
                        kembalian = bayar - total_bayar_diskon

                        # CUSTOMER
                        customer, _ = Customer.objects.get_or_create(nama=nama_input)

                        # PESANAN
                        pesanan = Pesanan.objects.create(
                            customer=customer,
                            total_harga=total_bayar_diskon,
                            tanggal=timezone.now()
                        )

                        # DETAIL PESANAN + STOK
                        for item in cart:
                            menu_item = MenuItem.objects.get(id=item["id"])
                            PesananDetail.objects.create(
                                pesanan=pesanan,
                                customer=customer,
                                menu=menu_item,
                                jumlah=item["qty"],
                                total_harga=item["total"]
                            )
                            # Kurangi stok
                            for bahan in MenuItemBahan.objects.filter(menu_item=menu_item):
                                bahan.kurangi_stok(item["qty"])

                        # RIWAYAT
                        Riwayat.objects.create(
                            customer=customer,
                            total_belanja=total_bayar_diskon,
                            pesanan=cart,
                            timestamp=timezone.now()
                        )

                        # MEMBER -> tambah point
                        if member_obj:
                            point = total_bayar_diskon // 10000
                            member_obj.point += point
                            member_obj.save()
                            messages.success(request, f"Point +{point}")

                        # Kosongkan cart
                        request.session["cart"] = []
                        request.session["kembalian"] = kembalian
                        messages.success(request, f"Transaksi berhasil. Kembalian: Rp{kembalian:,}")
                        return redirect("customer:menu")

                except Exception as e:
                    error = f"Terjadi kesalahan: {e}"

    total_bayar = sum(item["total"] for item in cart)
    if member_obj:
        diskon = int(total_bayar * 0.05)
        total_bayar_diskon = total_bayar - diskon
    else:
        total_bayar_diskon = total_bayar

    return render(request, "customer/menu.html", {
        "menu": menu,
        "cart": cart,
        "error": error,
        "total_bayar": total_bayar,
        "diskon": diskon,
        "total_bayar_diskon": total_bayar_diskon,
        "kembalian": kembalian,
        "member": member_obj,
        "nama_input": nama_input
    })


# Halaman Manajemen Member
def manajemen_member(request):
    members = Member.objects.all().order_by("id")
    return render(request, "customer/manajemen_member.html", {"members": members})

@csrf_exempt
def tambah_member_ajax(request):
    if request.method == "POST":
        nama = request.POST.get("nama", "").strip()
        umur = request.POST.get("umur", "").strip()
        pekerjaan = request.POST.get("pekerjaan", "").strip()

        if not nama or not umur or not pekerjaan:
            return JsonResponse({"success": False, "error": "Semua field harus diisi."})

        if not umur.isdigit():
            return JsonResponse({"success": False, "error": "Umur harus berupa angka."})

        if Member.objects.filter(nama__iexact=nama).exists():
            return JsonResponse({"success": False, "error": "Nama sudah terdaftar."})

        member = Member.objects.create(
            nama=nama,
            umur=int(umur),
            pekerjaan=pekerjaan
        )

        return JsonResponse({
            "success": True,
            "member": {
                "id": member.id,
                "nama": member.nama,
                "umur": member.umur,
                "pekerjaan": member.pekerjaan,
                "created_at": member.created_at.strftime("%d/%m/%Y")
            }
        })

    return JsonResponse({"success": False, "error": "Invalid request"})


# Tambah Menu
def tambah_menu_view(request):
    if request.method == "POST":
        nama = request.POST.get("nama")
        harga = request.POST.get("harga")

        if not nama or not harga:
            messages.error(request, "Nama & harga wajib diisi.")
            return redirect("customer:tambah_menu")

        if MenuItem.objects.filter(nama__iexact=nama).exists():
            messages.error(request, "Menu sudah ada.")
            return redirect("customer:tambah_menu")

        MenuItem.objects.create(nama=nama, harga=harga)
        messages.success(request, f"Menu {nama} ditambahkan.")
        return redirect("customer:menu")

    return render(request, "customer/tambah_menu.html")


# Riwayat Transaksi
def riwayat_view(request):
    riwayat_list = Riwayat.objects.all().order_by("-timestamp")
    return render(request, "customer/riwayat.html", {"riwayat_list": riwayat_list})
