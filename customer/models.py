from django.db import models

class MenuItem(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    harga = models.IntegerField()

    def __str__(self):
        return f"{self.nama} - Rp{self.harga:,}"

class Customer(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    saldo = models.IntegerField(default=0)

    def __str__(self):
        return self.nama

class Riwayat(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="riwayat")

    jenis = models.CharField(max_length=20)     
    saldo_awal = models.IntegerField()
    saldo_akhir = models.IntegerField()

    total_belanja = models.IntegerField(null=True, blank=True)
    perubahan = models.IntegerField(null=True, blank=True)

    pesanan = models.JSONField(null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.nama} ({self.jenis})"
