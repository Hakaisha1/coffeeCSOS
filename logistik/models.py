from django.db import models

class pegawai(models.Model):
  id_pegawai = models.CharField(max_length=10, unique=True)
  nama = models.CharField(max_length=100)
  posisi = models.CharField(max_length=50)
  shift = models.CharField(max_length=100)
  gaji_per_jam = models.IntegerField()
  jam_kerja = models.IntegerField(default=0) 

  def hitung_gaji(self):
    return self.jam_kerja * self.gaji_per_jam

  def __str__(self):
    return {self.nama}
  
class barista(pegawai):
  bonus_per_minuman = models.IntegerField(default=0)
  miuman_terjual = models.IntegerField(default=0) 

  def hitung_gaji(self):
    gaji_dasar =  super().hitung_gaji()
    return gaji_dasar + (self.miuman_terjual * self.bonus_per_minuman)
  