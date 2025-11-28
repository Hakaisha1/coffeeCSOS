import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coffeeCSOS.settings")  
django.setup()

from django.db import models


class Customer(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    saldo = models.IntegerField(default=0)

    class Meta:
        app_label = 'customer'  

    def __str__(self):
        return self.nama

class Riwayat(models.Model):
    JENIS_CHOICES = [
        ('top up', 'Top Up'),
        ('pembelian', 'Pembelian'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    jenis = models.CharField(max_length=20, choices=JENIS_CHOICES)
    saldo_awal = models.IntegerField()
    perubahan = models.IntegerField(null=True, blank=True)
    total_belanja = models.IntegerField(null=True, blank=True)
    saldo_akhir = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'customer'

class PesananDetail(models.Model):
    riwayat = models.ForeignKey(Riwayat, on_delete=models.CASCADE)
    menu = models.CharField(max_length=100)
    jumlah = models.IntegerField()
    subtotal = models.IntegerField()

    class Meta:
        app_label = 'customer'

class MenuItem:
    def __init__(self, nama, harga):
        self.nama = nama
        self.harga = harga

    def __str__(self):
        return f"{self.nama} - Rp{self.harga:,}"

class Pesanan:
    def __init__(self):
        self.daftar_pesanan = []
        self.total = 0

    def tambah_item(self, item, jumlah):
        subtotal = item.harga * jumlah
        self.daftar_pesanan.append((item, jumlah, subtotal))
        self.total += subtotal

    def tampilkan(self):
        print("\n=== Detail Pesanan ===")
        for item, jumlah, subtotal in self.daftar_pesanan:
            print(f"{item.nama} x{jumlah} = Rp{subtotal:,}")
        print(f"Total: Rp{self.total:,}")

class CustomerLogic:
    def __init__(self, nama):
        self.customer, _ = Customer.objects.get_or_create(nama=nama)

    def update_saldo(self, jumlah):
        self.customer.saldo = jumlah
        self.customer.save()

    def top_up(self, jumlah):
        saldo_awal = self.customer.saldo
        saldo_akhir = saldo_awal + jumlah

        Riwayat.objects.create(
            customer=self.customer,
            jenis='top up',
            saldo_awal=saldo_awal,
            perubahan=jumlah,
            saldo_akhir=saldo_akhir
        )

        self.update_saldo(saldo_akhir)
        return saldo_akhir

    def bayar(self, pesanan: Pesanan):
        if self.customer.saldo < pesanan.total:
            return False

        saldo_awal = self.customer.saldo
        saldo_akhir = saldo_awal - pesanan.total

        riwayat = Riwayat.objects.create(
            customer=self.customer,
            jenis='pembelian',
            saldo_awal=saldo_awal,
            total_belanja=pesanan.total,
            saldo_akhir=saldo_akhir
        )

        for item, jumlah, subtotal in pesanan.daftar_pesanan:
            PesananDetail.objects.create(
                riwayat=riwayat,
                menu=item.nama,
                jumlah=jumlah,
                subtotal=subtotal
            )

        self.update_saldo(saldo_akhir)
        return True

    def lihat_riwayat(self):
        data = Riwayat.objects.filter(customer=self.customer).order_by('created_at')
        if not data:
            print("Belum ada riwayat.")
            return

        print(f"\n=== Riwayat Transaksi {self.customer.nama} ===")
        for i, r in enumerate(data, 1):
            print(f"\n--- Transaksi {i} ---")
            print(f"Jenis        : {r.jenis}")
            print(f"Saldo Awal   : Rp{r.saldo_awal:,}")
            if r.jenis == 'top up':
                print(f"Top Up       : Rp{r.perubahan:,}")
            else:
                print(f"Total Belanja: Rp{r.total_belanja:,}")
                print("Detail Pesanan:")
                for d in PesananDetail.objects.filter(riwayat=r):
                    print(f" - {d.menu} x{d.jumlah} = Rp{d.subtotal:,}")
            print(f"Saldo Akhir  : Rp{r.saldo_akhir:,}")

def main():
    menu = [
        MenuItem("Espresso", 20000),
        MenuItem("Ice Cafe Latte", 25000),
        MenuItem("Cappuccino", 23000),
        MenuItem("Matcha Latte", 27500),
        MenuItem("Butterscotch Coffee", 32000)
    ]

    nama = input("Masukkan nama customer: ")
    cust = CustomerLogic(nama)

    while True:
        print("\n=== MENU UTAMA ===")
        print("1. Buat Pesanan")
        print("2. Lihat Riwayat")
        print("3. Top Up")
        print("0. Keluar")
        pilih = input("Pilih menu: ")

        if pilih == "1":
            pesanan = Pesanan()
            print("\n=== MENU ===")
            for i, item in enumerate(menu, 1):
                print(f"{i}. {item}")
            while True:
                pilih_menu = int(input("Pilih menu (0 selesai): "))
                if pilih_menu == 0:
                    break
                jumlah = int(input("Jumlah: "))
                pesanan.tambah_item(menu[pilih_menu-1], jumlah)

            if pesanan.daftar_pesanan:
                pesanan.tampilkan()
                if cust.bayar(pesanan):
                    print("Pembayaran berhasil!")
                else:
                    print("Saldo tidak cukup.")

        elif pilih == "2":
            cust.lihat_riwayat()

        elif pilih == "3":
            jumlah = int(input("Masukkan jumlah top up: "))
            saldo = cust.top_up(jumlah)
            print(f"Saldo sekarang: Rp{saldo:,}")

        elif pilih == "0":
            print("Terima kasih!")
            break

if __name__ == "__main__":
    main()
