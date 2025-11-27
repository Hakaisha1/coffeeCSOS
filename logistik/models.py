from django.db import models

class Barang(models.Model):
    nama = models.CharField(max_length=100)
    stok = models.IntegerField(default=0)
    harga = models.IntegerField(default=0)
    kadaluarsa = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nama


class Supplier(models.Model):
    nama = models.CharField(max_length=100)
    kontak = models.CharField(max_length=100)

    def __str__(self):
        return self.nama
