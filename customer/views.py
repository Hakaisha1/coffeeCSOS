from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer, MenuItem, Pesanan, PesananDetail, Riwayat
from django.utils import timezone
from .models import MenuItemBahan
from logistik.models import Barang

def menu_view(request):
    menu = MenuItem.objects.all()
    cart = request.session.get('cart', [])
    error = None
    success = None
    kembalian = None

    customer = Customer.objects.first()
    if not customer:
        error = "Belum ada customer. Silakan tambahkan customer terlebih dahulu."
        return render(request, 'customer/menu.html', {
            'menu': menu,
            'cart': cart,
            'error': error,
            'success': success,
            'total_bayar': 0,
            'kembalian': kembalian,
            'customer': None
        })

    if request.method == "POST":
        # Tambah item ke keranjang
        if 'add_item' in request.POST:
            item_id = int(request.POST.get('item_id'))
            qty = int(request.POST.get('qty', 1))
            menu_item = MenuItem.objects.get(id=item_id)
            found = False
            for c in cart:
                if c['id'] == item_id:
                    c['qty'] += qty
                    c['total'] = c['harga'] * c['qty']
                    found = True
                    break
            if not found:
                cart.append({
                    'id': menu_item.id,
                    'nama': menu_item.nama,
                    'harga': menu_item.harga,
                    'qty': qty,
                    'total': menu_item.harga * qty
                })
            request.session['cart'] = cart
            success = f"{menu_item.nama} x{qty} ditambahkan ke keranjang."

        # Update jumlah item
        elif 'update_qty' in request.POST:
            item_id = int(request.POST.get('item_id'))
            qty = int(request.POST.get('qty', 1))
            for c in cart:
                if c['id'] == item_id:
                    c['qty'] = qty
                    c['total'] = c['harga'] * qty
                    success = f"Jumlah {c['nama']} diperbarui menjadi {qty}."
                    break
            request.session['cart'] = cart

        # Hapus item
        elif 'hapus_item' in request.POST:
            item_id = int(request.POST.get('item_id'))
            cart = [c for c in cart if c['id'] != item_id]
            request.session['cart'] = cart
            success = "Item dihapus dari keranjang."

        # Checkout / Bayar
        elif 'checkout' in request.POST:
            total_bayar = sum(item['total'] for item in cart)
            try:
                bayar = int(request.POST.get('bayar', 0))
            except ValueError:
                error = "Uang bayar harus berupa angka."
                bayar = 0

            if bayar < total_bayar:
                error = f"Uang bayar kurang! Total Rp{total_bayar:,}."
            else:
                kembalian = bayar - total_bayar

                # Simpan pesanan ringkas
                pesanan = Pesanan.objects.create(
                    customer=customer,
                    total_harga=total_bayar
                )

                # Simpan detail tiap item
                detail_list = []
                for item in cart:
                    menu_item = MenuItem.objects.get(id=item['id'])
                    detail = PesananDetail.objects.create(
                        customer=customer,
                        menu=menu_item,
                        jumlah=item['qty'],
                        total_harga=item['total']
                    )
                    detail_list.append({
                        'menu': detail.menu.nama,
                        'qty': detail.jumlah,
                        'total': detail.total_harga
                    })

                # Simpan riwayat transaksi
                Riwayat.objects.create(
                    customer=customer,
                    total_belanja=total_bayar,
                    perubahan=kembalian,
                    pesanan=detail_list
                )

                cart = []
                request.session['cart'] = cart
                success = f"Transaksi berhasil. Kembalian: Rp{kembalian:,}."

    total_bayar = sum(item['total'] for item in cart)

    return render(request, 'customer/menu.html', {
        'menu': menu,
        'cart': cart,
        'error': error,
        'success': success,
        'total_bayar': total_bayar,
        'kembalian': kembalian,
        'customer': customer
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
        return redirect("menu")  # atau redirect ke halaman menu

    return render(request, "customer/tambah_menu.html")


# ============================
# Halaman Riwayat Transaksi
# ============================
def riwayat_view(request):
    customer = Customer.objects.first()  # nanti bisa diganti sesuai user login
    if not customer:
        messages.error(request, "Belum ada customer.")
        return redirect('menu_view')

    riwayat_list = Riwayat.objects.filter(customer=customer).order_by('-timestamp')

    context = {'riwayat_list': riwayat_list}
    return render(request, "customer/riwayat.html", context)

