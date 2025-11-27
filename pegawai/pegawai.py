import json

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
  

class barista(pegawai):
  def __init__(self, id_pegawai, nama, shift, gaji_per_jam, bonus_per_minuman):
    super().__init__(id_pegawai, nama, "Barista", shift, gaji_per_jam)
    
    self.bonus_per_minuman = bonus_per_minuman 
    self.minuman_terjual = 0

  def tambah_penjualan(self, jumlah):
    self.minuman_terjual += jumlah

  def hitung_gaji(self):
    gaji_dasar =  super().hitung_gaji()
    bonus = self.minuman_terjual * self.bonus_per_minuman
    return gaji_dasar + bonus

  def tampilkan_info(self):
    super().tampilkan_info()
    print(f'Minuman terjual : {self.minuman_terjual}')
    print(f'Bonus per cup   : Rp. {self.bonus_per_minuman}')
    print(f'Gaji + bonus    : Rp. {self.hitung_gaji()}')
    print('=' * 30)

  def database(self):
    data = super().database()
    data.update({
      'bonus_per_minuman': self.bonus_per_minuman,
      'minuman_terjual': self.minuman_terjual,
      'jenis': 'barista'
    })
    return data

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
  
  def tampilkan_info(self):
    super().tampilkan_info()
    print(f'Minuman terjual : {self.minuman_terjual}')
    print(f'Bonus per cup   : Rp. {self.bonus_per_minuman}')
    print(f'Gaji + bonus    : Rp. {self.hitung_gaji()}')
    print('=' * 30)

  def tampilkan_semua(self):
    if not self.daftar_pegawai:
      print('Belum ada daftar pegawai')
      return
    print('=== Data semua pegawai ===')
    for peg in self.daftar_pegawai:
      peg.tampilkan_info()

  def simpan_data(self, filename):
    data = [pegawai.database() for pegawai in self.daftar_pegawai]
    with open(filename, 'w') as f:
      json.dump(data, f, indent=4)

  def get_json(self, filename):
    with open(filename, 'r') as f:
      data = json.load(f)

    for item in data:
      if item.get('jenis') == 'barista':
        peg = barista(
          item['id_pegawai'], item['nama'],
          item['shift'], item['gaji_per_jam'],
          item['bonus_per_minuman']
        )
      peg.jam_kerja = item['jam_kerja']
      peg.minuman_terjual = item['minuman_terjual']
      self.daftar_pegawai.append(peg)


b1 = barista('111', 'Andi', 'Pagi', 15000, 1000)
b1.tambah_jam_kerja(6)
b1.tambah_penjualan(20)

b2 = barista('112', 'Bahlil', 'Pagi, Siang, Sore, Malam', 500, 1000)
b2.tambah_jam_kerja(24)
b2.tambah_penjualan(30)

m = manajemen_pegawai()
m.tambah_pegawai(b1)
m.tambah_pegawai(b2)

m.simpan_data('assets/database/pegawai.json')

hasil = m.cari_pegawai('111')

if hasil:
  print('Pegawai ditemukan!')
  print('-' * 30)
  hasil.tampilkan_info()

else:
  print('Pegawai tidak ditemukan!')
  print('-' * 30)
  print('-' * 30)

m.tampilkan_semua()
