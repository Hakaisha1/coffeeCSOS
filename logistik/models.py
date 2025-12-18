from django.db import models



class Supplier(models.Model):
    nama = models.CharField(max_length=100)
    Barang = models.CharField(max_length=100, default='')
    kontak = models.CharField(max_length=100)

    def __str__(self):
        return self.nama

class Barang(models.Model):
    nama = models.CharField(max_length=100)  # "Kopi Espresso (18g/unit)"
    stok = models.IntegerField()  # dalam unit
    stok_minimum = models.IntegerField()
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    kadaluarsa = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nama

