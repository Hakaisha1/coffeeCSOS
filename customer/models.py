from django.db import models
from logistik.models import Barang


class MenuItem(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    harga = models.IntegerField()

    def __str__(self):
        return f"{self.nama} - Rp{self.harga:,}"


class Customer(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama


class Riwayat(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="riwayat")
    total_belanja = models.IntegerField(null=True, blank=True)
    perubahan = models.IntegerField(null=True, blank=True)
    pesanan = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        total = self.total_belanja or 0
        return f"Riwayat {self.id} - {self.customer.nama} (Rp{total:,})"


class PesananDetail(models.Model):
    pesanan = models.ForeignKey(
        "Pesanan",
        on_delete=models.CASCADE,
        related_name="detail"
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    menu = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    jumlah = models.IntegerField()
    total_harga = models.IntegerField()
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.menu.nama} x {self.jumlah}"


class Pesanan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_harga = models.IntegerField(default=0)
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pesanan {self.id} - {self.customer.nama}"


class MenuItemBahan(models.Model):
    menu_item = models.ForeignKey(MenuItem, related_name='bahan_baku', on_delete=models.CASCADE)
    barang = models.ForeignKey(Barang, on_delete=models.PROTECT)
    jumlah_dibutuhkan = models.IntegerField(default=1)

    def kurangi_stok(self, jumlah_pesanan):
        total_unit = self.jumlah_dibutuhkan * jumlah_pesanan
        if self.barang.stok < total_unit:
            raise ValueError(
                f"Stok {self.barang.nama} tidak cukup "
                f"(tersisa {self.barang.stok}, butuh {total_unit})"
            )
        self.barang.stok -= total_unit
        self.barang.save()


class Member(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    pekerjaan = models.CharField(max_length=100, blank=True)
    umur = models.PositiveIntegerField(null=True, blank=True)
    point = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # tambahkan ini

    def __str__(self):
        return f"{self.nama} ({self.point} point)"



class RatingMenu(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    menu = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.nama} - {self.menu.nama} ({self.rating})"


class RatingCoffeeshop(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    komentar = models.TextField(blank=True)
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.nama} - {self.rating}"
