from django.db import models
from django.utils import timezone
from decimal import Decimal
from datetime import datetime, date, time, timedelta 

class Pegawai(models.Model):
    id_pegawai = models.CharField(max_length=10, unique=True, primary_key=True)
    nama = models.CharField(max_length=100)
    posisi = models.CharField(max_length=50)
    shift = models.CharField(max_length=100)
    gaji_per_jam = models.DecimalField(max_digits=10, decimal_places=2)
    jam_kerja = models.IntegerField(default=0) # Ini akan diupdate dari Absensi
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

class Absensi(models.Model):
    JENIS_CHOICES = [
        ('barista', 'Barista'),
        ('waiter', 'Waiter'),
        ('cleaner', 'Cleaner'),
    ]

    jenis = models.CharField(max_length=10, choices=JENIS_CHOICES)
    id_pegawai = models.CharField(max_length=10)
    tanggal = models.DateField(default=timezone.now)
    jam_masuk = models.TimeField()
    jam_pulang = models.TimeField()

    jam_kerja = models.IntegerField(default=0, editable=False)
    jam_lembur_malam = models.IntegerField(default=0, editable=False)
    gaji_harian = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pegawai_absensi'

    def __str__(self):
        return f"{self.id_pegawai} - {self.tanggal} ({self.jam_kerja} jam, lembur {self.jam_lembur_malam} jam)"

    def save(self, *args, **kwargs):
        from datetime import datetime, date, time, timedelta

        base_date = self.tanggal or date.today()
        dt_masuk = datetime.combine(base_date, self.jam_masuk)
        dt_pulang = datetime.combine(base_date, self.jam_pulang)

        self.jam_kerja = 0
        self.jam_lembur_malam = 0
        self.gaji_harian = Decimal('0')

        if dt_pulang < dt_masuk:
            dt_pulang += timedelta(days=1)
            
        durasi_detik = (dt_pulang - dt_masuk).total_seconds()
        durasi_jam_float = durasi_detik / 3600
        self.jam_kerja = int(round(durasi_jam_float)) 

        shift_malam_start = time(21, 0) 
        shift_malam_end = time(6, 0)    

        total_lembur_malam_detik = 0

        current_dt_iterator = dt_masuk
        while current_dt_iterator < dt_pulang:

            is_malam = False
            if current_dt_iterator.time() >= shift_malam_start or current_dt_iterator.time() < shift_malam_end:
                is_malam = True
            
            if is_malam:
                total_lembur_malam_detik += 60 
            
            current_dt_iterator += timedelta(minutes=1)

        self.jam_lembur_malam = int(round(total_lembur_malam_detik / 3600))


        model_map = {
            'barista': Barista,
            'waiter': Waiter,
            'cleaner': Cleaner,
        }
        gaji_per_jam_dasar = Decimal('0')
        bonus_per_jam_lembur = Decimal('0') 
        Model = model_map.get(self.jenis)

        if Model is not None:
            try:
                obj = Model.objects.get(id_pegawai=self.id_pegawai)
                gaji_per_jam_dasar = obj.gaji_per_jam
                if hasattr(obj, 'bonus_per_jam'):
                    bonus_per_jam_lembur = obj.bonus_per_jam
                
               
            except Model.DoesNotExist:
                pass

        self.gaji_harian = (Decimal(self.jam_kerja) * gaji_per_jam_dasar) + \
                           (Decimal(self.jam_lembur_malam) * bonus_per_jam_lembur)

        super().save(*args, **kwargs)