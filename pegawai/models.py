from django.db import models

class Pegawai(models.Model):
    id_pegawai = models.CharField(max_length=10, unique=True, primary_key=True)
    nama = models.CharField(max_length=100)
    posisi = models.CharField(max_length=50)
    shift = models.CharField(max_length=100)
    gaji_per_jam = models.DecimalField(max_digits=10, decimal_places=2)
    jam_kerja = models.IntegerField(default=0)
    jenis = models.CharField(max_length=20, default='pegawai')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = 'pegawai_pegawai'
    
    def __str__(self):
        return f"{self.nama} - {self.posisi}"


class Barista(models.Model):
    id_pegawai = models.CharField(max_length=10, unique=True, primary_key=True)
    nama = models.CharField(max_length=100)
    shift = models.CharField(max_length=100)
    gaji_per_jam = models.DecimalField(max_digits=10, decimal_places=2)
    bonus_per_jam = models.DecimalField(max_digits=10, decimal_places=2)
    jumlah_jam = models.IntegerField(default=0)
    jam_kerja = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = 'pegawai_barista'
    
    def __str__(self):
        return f"{self.nama} - Barista"
    
class Waiter(models.Model):
    id_pegawai = models.CharField(max_length=10, unique=True, primary_key=True)
    nama = models.CharField(max_length=100)
    shift = models.CharField(max_length=100)
    gaji_per_jam = models.DecimalField(max_digits=10, decimal_places=2)
    bonus_per_jam = models.DecimalField(max_digits=10, decimal_places=2)
    jumlah_jam = models.IntegerField(default=0)
    jam_kerja = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = 'pegawai_waiter'
    
    def __str__(self):
        return f"{self.nama} - Waiter"

class Cleaner(models.Model):
    id_pegawai = models.CharField(max_length=10, unique=True, primary_key=True)
    nama = models.CharField(max_length=100)
    shift = models.CharField(max_length=100)
    gaji_per_jam = models.DecimalField(max_digits=10, decimal_places=2)
    bonus_per_jam = models.DecimalField(max_digits=10, decimal_places=2)
    jumlah_jam = models.IntegerField(default=0)
    jam_kerja = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = 'pegawai_cleaner'
    
    def __str__(self):
        return f"{self.nama} - Cleaner"