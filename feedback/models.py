from django.db import models


class Feedback(models.Model):
    """Model untuk menyimpan feedback customer tanpa login"""
    
    RATING_CHOICES = [(i, f"{i} Bintang") for i in range(1, 6)]
    
    KATEGORI_CHOICES = [
        ('pelayanan', 'Pelayanan'),
        ('rasa', 'Rasa Kopi'),
        ('suasana', 'Suasana'),
        ('harga', 'Harga'),
        ('kebersihan', 'Kebersihan'),
        ('lainnya', 'Lainnya'),
    ]
    
    UMUR_CHOICES = [
        ('<12', 'Di bawah 12 tahun'),
        ('12-17', '12-17 tahun'),
        ('18-24', '18-24 tahun'),
        ('25-34', '25-34 tahun'),
        ('35-44', '35-44 tahun'),
        ('45-54', '45-54 tahun'),
        ('55+', '55 tahun ke atas'),
    ]
    
    # Data customer (optional, tanpa login)
    nama = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nama (Opsional)")
    umur = models.CharField(max_length=10, choices=UMUR_CHOICES, blank=True, null=True, verbose_name="Umur (Opsional)")
    nomor_meja = models.CharField(max_length=10, blank=True, null=True, verbose_name="Nomor Meja")
    
    # Rating & Feedback
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Rating")
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES, verbose_name="Kategori Feedback")
    komentar = models.TextField(verbose_name="Komentar")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Tanggal")
    is_read = models.BooleanField(default=False, verbose_name="Sudah Dibaca")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback Pelanggan"
    
    def __str__(self):
        nama_display = self.nama or "Anonim"
        return f"{nama_display} - {self.rating} Bintang - {self.get_kategori_display()}"
    
    def get_star_display(self):
        """Return star emoji untuk rating"""
        return "⭐" * self.rating
