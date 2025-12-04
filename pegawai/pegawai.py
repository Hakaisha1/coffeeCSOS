import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coffeeCSOS.settings')
django.setup()

from pegawai.models import Pegawai as PegawaiModel, Barista as BaristaModel

class pegawai:
  def __init__(self, id_pegawai, nama, posisi, shift, gaji_per_jam):
    self.nama = nama
    self.id_pegawai = id_pegawai
    self.posisi = posisi
    self.shift = shift
    self.gaji_per_jam = gaji_per_jam
    self.jam_kerja = 0

  def tambah_jam_kerja(self, jam):
    self.jam_kerja += jam

  def hitung_gaji(self):
    return self.jam_kerja * self.gaji_per_jam
    
  def tampilkan_info(self):
    print(f'ID Pegawai : {self.id_pegawai} ')
    print(f'Nama       : {self.nama} ')
    print(f'Posisi     : {self.posisi} ')
    print(f'Shift      : {self.shift} ')
    print('-' * 30)

  def database(self):
    return {
      'id_pegawai': self.id_pegawai,
      'nama': self.nama,
      'posisi': self.posisi,
      'shift': self.shift,
      'gaji_per_jam': self.gaji_per_jam,
      'jam_kerja': self.jam_kerja,
    }
  
  def simpan_ke_db(self):
    PegawaiModel.objects.update_or_create(
      id_pegawai=self.id_pegawai,
      defaults={
        'nama': self.nama,
        'posisi': self.posisi,
        'shift': self.shift,
        'gaji_per_jam': self.gaji_per_jam,
        'jam_kerja': self.jam_kerja,
        'jenis': 'pegawai'
      }
    )

class barista(pegawai):
  def __init__(self, id_pegawai, nama, shift, gaji_per_jam, bonus_per_jam):
    super().__init__(id_pegawai, nama, "Barista", shift, gaji_per_jam)
    
    self.bonus_per_jam = bonus_per_jam 
    self.jumlah_jam = 0

  def bonus_gaji(self, jumlah):
    self.jumlah_jam += jumlah

  def hitung_gaji(self):
    gaji_dasar =  super().hitung_gaji()
    bonus = self.jumlah_jam * self.bonus_per_jam
    return gaji_dasar + bonus

  def tampilkan_info(self):
    super().tampilkan_info()
    print(f'Minuman terjual : {self.jumlah_jam}')
    print(f'Bonus per cup   : Rp. {self.bonus_per_jam}')
    print(f'Gaji + bonus    : Rp. {self.hitung_gaji()}')
    print('=' * 30)

  def database(self):
    data = super().database()
    data.update({
      'bonus_per_minuman': self.bonus_per_jam,
      'minuman_terjual': self.jumlah_jam,
      'jenis': 'barista'
    })
    return data

  def simpan_ke_db(self):
    BaristaModel.objects.update_or_create(
      id_pegawai=self.id_pegawai,
      defaults={
        'nama': self.nama,
        'shift': self.shift,
        'gaji_per_jam': self.gaji_per_jam,
        'bonus_per_jam': self.bonus_per_jam,
        'jumlah_jam': self.jumlah_jam,
        'jam_kerja': self.jam_kerja,
      }
    )

class waiter(pegawai):
  def __init__(self, id_pegawai, nama, shift, gaji_per_jam, bonus_per_jam):
    super().__init__(id_pegawai, nama, "Waiter", shift, gaji_per_jam)
    
    self.bonus_per_jam = bonus_per_jam
    self.jumlah_jam = 0

  def bonus_gaji(self, jumlah):
    self.jumlah_jam += jumlah

  def hitung_gaji(self):
    gaji_dasar =  super().hitung_gaji()
    bonus = self.jumlah_jam * self.bonus_per_jam
    return gaji_dasar + bonus

  def tampilkan_info(self):
    super().tampilkan_info()
    print(f'Minuman terjual : {self.jumlah_jam}')
    print(f'Bonus per cup   : Rp. {self.bonus_per_jam}')
    print(f'Gaji + bonus    : Rp. {self.hitung_gaji()}')
    print('=' * 30)

  def database(self):
    data = super().database()
    data.update({
      'bonus_per_minuman': self.bonus_per_jam,
      'minuman_terjual': self.jumlah_jam,
      'jenis': 'waiter'
    })
    return data

  def simpan_ke_db(self):
    BaristaModel.objects.update_or_create(
      id_pegawai=self.id_pegawai,
      defaults={
        'nama': self.nama,
        'shift': self.shift,
        'gaji_per_jam': self.gaji_per_jam,
        'bonus_per_jam': self.bonus_per_jam,
        'jumlah_jam': self.jumlah_jam,
        'jam_kerja': self.jam_kerja,
      }
    )

class cleaner(pegawai):
  def __init__(self, id_pegawai, nama, shift, gaji_per_jam, bonus_per_jam):
    super().__init__(id_pegawai, nama, "Cleaner", shift, gaji_per_jam)
    
    self.bonus_per_jam = bonus_per_jam
    self.jumlah_jam = 0

  def bonus_gaji(self, jumlah):
    self.jumlah_jam += jumlah

  def hitung_gaji(self):
    gaji_dasar =  super().hitung_gaji()
    bonus = self.jumlah_jam * self.bonus_per_jam
    return gaji_dasar + bonus

  def tampilkan_info(self):
    super().tampilkan_info()
    print(f'Minuman terjual : {self.jumlah_jam}')
    print(f'Bonus per cup   : Rp. {self.bonus_per_jam}')
    print(f'Gaji + bonus    : Rp. {self.hitung_gaji()}')
    print('=' * 30)

  def database(self):
    data = super().database()
    data.update({
      'bonus_per_minuman': self.bonus_per_jam,
      'minuman_terjual': self.jumlah_jam,
      'jenis': 'cs'
    })
    return data

  def simpan_ke_db(self):
    BaristaModel.objects.update_or_create(
      id_pegawai=self.id_pegawai,
      defaults={
        'nama': self.nama,
        'shift': self.shift,
        'gaji_per_jam': self.gaji_per_jam,
        'bonus_per_jam': self.bonus_per_jam,
        'jumlah_jam': self.jumlah_jam,
        'jam_kerja': self.jam_kerja,
      }
    )


class manajemen_pegawai:
  def __init__(self):
    self.daftar_pegawai = []

  def tambah_pegawai(self, pegawai):
    self.daftar_pegawai.append(pegawai)

  def cari_pegawai(self, id_pegawai):
    for pegawai in self.daftar_pegawai:
      if pegawai.id_pegawai == id_pegawai:
        return pegawai
    return None
  
  def tampilkan_semua(self):
    if not self.daftar_pegawai:
      print('Belum ada daftar pegawai')
      return
    print('=== Data semua pegawai ===')
    for peg in self.daftar_pegawai:
      peg.tampilkan_info()


  def load_dari_database(self):
    barista_objs = BaristaModel.objects.all()
    for b in barista_objs:
      peg = barista(b.id_pegawai, b.nama, b.shift, float(b.gaji_per_jam), float(b.bonus_per_jam))
      peg.jam_kerja = b.jam_kerja
      peg.jumlah_jam = b.jumlah_jam
      self.daftar_pegawai.append(peg)
    
    waiter_objs = WaiterModel.objects.all()
    for w in waiter_objs:
      peg = waiter(w.id_pegawai, w.nama, w.shift, float(w.gaji_per_jam), float(w.bonus_per_jam))
      peg.jam_kerja = w.jam_kerja
      peg.jumlah_jam = w.jumlah_jam
      self.daftar_pegawai.append(peg)

    cleaner_objs = CleanerModel.objects.all()
    for c in cleaner_objs:
      peg = cleaner(c.id_pegawai, c.nama, c.shift, float(c.gaji_per_jam), float(c.bonus_per_jam))
      peg.jam_kerja = c.jam_kerja
      peg.jumlah_jam = c.jumlah_jam
      self.daftar_pegawai.append(peg)

    pegawai_objs = PegawaiModel.objects.filter(jenis='pegawai')
    for p in pegawai_objs:
      peg = pegawai(p.id_pegawai, p.nama, p.posisi, p.shift, float(p.gaji_per_jam))
      peg.jam_kerja = p.jam_kerja
      self.daftar_pegawai.append(peg)
    
    print(f'{len(self.daftar_pegawai)} pegawai berhasil dimuat dari database')


if __name__ == '__main__':
  b1 = barista('111', 'Andi', 'Pagi', 15000, 1000)
  b1.tambah_jam_kerja(6)
  b1.bonus_gaji(20)

  b2 = barista('112', 'Bahlil', 'Pagi, Siang, Sore, Malam', 15000, 1000)
  b2.tambah_jam_kerja(24)
  b2.bonus_gaji(6)

  w1 = waiter('113', 'Dodo', 'Pagi, Siang', 15000, 1000)
  w1.tambah_jam_kerja(12)

  w2 = waiter('114', 'Umar', 'Sore, Malam', 15000, 1000)
  w2.tambah_jam_kerja(12)
  w2.bonus_gaji(6)

  cs1 = cleaner('115', 'Tono', 'Siang, Sore, Malam', 15000, 1000)
  cs1.tambah_jam_kerja(15)
  cs1.bonus_gaji(6)
  
  cs2 = cleaner('116', 'Joni', 'Pagi, Siang, Sore, Malam', 15000, 1000)
  cs2.tambah_jam_kerja(24)
  cs2.bonus_gaji(6)

  m = manajemen_pegawai()
  m.tambah_pegawai(b1)
  m.tambah_pegawai(b2)
  m.tambah_pegawai(w1)
  m.tambah_pegawai(w2)
  m.tambah_pegawai(cs1)
  m.tambah_pegawai(cs2)
  
  m.simpan_ke_database()

  hasil = m.cari_pegawai('111')

  if hasil:
    print('Pegawai ditemukan!')
    print('-' * 30)
    hasil.tampilkan_info()
  else:
    print('Pegawai tidak ditemukan!')
    print('-' * 30)

  m.tampilkan_semua()
  