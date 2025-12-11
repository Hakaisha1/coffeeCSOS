from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer, MenuItem, Pesanan, PesananDetail
from logistik.models import Barang
from customer.models import Riwayat
from django.utils import timezone


def menu_view(request):
    menu = MenuItem.objects.all()

    cart = request.session.get('cart', [])
    customer_id = request.session.get('customer_id')
    customer = Customer.objects.filter(id=customer_id).first() if customer_id else None

    error = None
    success = None
    kembalian = None

    # TAMBAH ITEM
    if request.method == "POST" and 'add_item' in request.POST:
        item_id = int(request.POST.get("item_id"))
        menu_item = MenuItem.objects.get(id=item_id)

        found = False
        for c in cart:
            if c['id'] == item_id:
                c['qty'] += 1
                c['total'] = c['qty'] * c['harga']
                found = True
                break

        if not found:
            cart.append({
                "id": menu_item.id,
                "nama": menu_item.nama,
                "harga": menu_item.harga,
                "qty": 1,
                "total": menu_item.harga
            })

        request.session["cart"] = cart
        success = f"{menu_item.nama} ditambahkan ke keranjang."

    # HAPUS ITEM
    if request.method == "POST" and "hapus_item" in request.POST:
        item_id = int(request.POST.get("item_id"))
        cart = [c for c in cart if c['id'] != item_id]
        request.session['cart'] = cart
        success = "Item dihapus dari keranjang."

    # UPDATE JUMLAH
    if request.method == "POST" and "update_qty" in request.POST:
        item_id = int(request.POST.get("item_id"))
        qty = int(request.POST.get("qty", 1))
        for c in cart:
            if c['id'] == item_id:
                c['qty'] = qty
                c['total'] = qty * c['harga']
                break
        request.session['cart'] = cart
        success = "Jumlah diperbarui."

    # CHECKOUT 
    if request.method == "POST" and "checkout" in request.POST:

        nama = request.POST.get("nama", "").strip()
        if not nama:
            error = "Nama customer wajib diisi untuk checkout."
        else:
            customer, created = Customer.objects.get_or_create(nama=nama)
            request.session["customer_id"] = customer.id

            total_bayar = sum(item['total'] for item in cart)
            bayar = int(request.POST.get("bayar", 0))

            if bayar < total_bayar:
                error = f"Uang bayar kurang! Total: Rp{total_bayar:,}"
            else:
                kembalian = bayar - total_bayar

                pesanan = Pesanan.objects.create(
                    customer=customer,
                    total_harga=total_bayar
                )

                for item in cart:
                    menu_item = MenuItem.objects.get(id=item['id'])
                    PesananDetail.objects.create(
                        customer=customer,
                        menu=menu_item,
                        jumlah=item['qty'],
                        total_harga=item['total']
                    )
                
                # Simpan ke Riwayat
                Riwayat.objects.create(
                    customer=customer,
                    jenis='pembelian',
                    total_belanja=total_bayar,
                    perubahan=kembalian,
                    pesanan=cart,  
                )


                cart = []
                request.session['cart'] = cart
                success = f"Transaksi berhasil. Kembalian: Rp{kembalian:,}"

    total_bayar = sum(item['total'] for item in cart)

    return render(request, "customer/menu.html", {
        "menu": menu,
        "cart": cart,
        "error": error,
        "success": success,
        "total_bayar": total_bayar,
        "kembalian": kembalian,
        "customer": customer,
    })




def tambah_menu_view(request):
    if request.method == "POST":
        nama = request.POST.get("nama")
        harga = request.POST.get("harga")
        bahan_text = request.POST.get("bahan")  # textarea

        if not nama or not harga or not bahan_text:
            messages.error(request, "Semua field wajib diisi.")
            return redirect("tambah_menu")

        # Buat menu baru
        menu_item, created = MenuItem.objects.get_or_create(
            nama=nama,
            defaults={"harga": harga}
        )

        if not created:
            messages.error(request, f"Menu {nama} sudah ada.")
            return redirect("tambah_menu")

        # Proses bahan
        bahan_list = [b.strip() for b in bahan_text.splitlines() if b.strip()]
        for bahan_nama in bahan_list:
            try:
                barang = Barang.objects.get(nama=bahan_nama)
                MenuItemBahan.objects.create(
                    menu_item=menu_item,
                    barang=barang,
                    jumlah_dibutuhkan=1
                )
            except Barang.DoesNotExist:
                messages.error(request, f"Barang {bahan_nama} tidak ditemukan di stok.")
                continue

        messages.success(request, f"Menu {nama} berhasil ditambahkan.")
        return redirect("menu")  

    return render(request, "customer/tambah_menu.html")

# Riwayat Transaksi
def riwayat_view(request):
    riwayat_list = Riwayat.objects.all().order_by('-timestamp')

    return render(request, "customer/riwayat.html", {
        "riwayat_list": riwayat_list
    })
