# Kode bagian logistik
import json

class Barang:
    def __init__(self, nama, stok, harga, kadaluarsa=None):
        self.nama = nama
        self.stok = stok
        self.harga = harga
        self.kadaluarsa = kadaluarsa

    def tambah_stok(self, jumlah):
        self.stok += jumlah

    def kurangi_stok(self, jumlah):
        if jumlah <= self.stok:
            self.stok -= jumlah
        else:
            print("Stok tidak cukup!")

    def info(self):
        kadaluarsa = self.kadaluarsa if self.kadaluarsa else "Tidak ada"
        return (
            f"Nama: {self.nama} | Stok: {self.stok} | Harga: {self.harga} | "
            f"Kadaluarsa: {kadaluarsa}"
        )
    


class supplier:
    def __init__(self, nama, kontak):
        self.nama = nama
        self.kontak = kontak

    def info(self):
        return f"Supplier: {self.nama} | Kontak: {self.kontak}"



class TransaksiPembelian:
    def __init__(self, supplier, barang, jumlah, tanggal):
        self.supplier = supplier #class supplier
        self.barang = barang    #class barang
        self.jumlah = jumlah
        self.tanggal = tanggal

    def proses(self):
        self.barang.tambah_stok(self.jumlah)  #method di class barang

    def info(self):
        return (
            f"Transaksi Pembelian: {self.jumlah} {self.barang.nama} "
            f"dari {self.supplier.nama} pada {self.tanggal}"
        )
    


class Gudang:
    def __init__(self):
        self.daftar_barang = []

    def tambah_barang(self, barang):
        self.daftar_barang.append(barang)

    def cari_barang(self, nama):
        hasil = []
        for barang in self.daftar_barang:
            if nama.lower() in barang.nama.lower():
                hasil.append(barang)
        return hasil

    def hapus_barang(self, nama):
        for barang in self.daftar_barang:
            if barang.nama.lower() == nama.lower():
                self.daftar_barang.remove(barang)
                print(f"{nama} berhasil dihapus.")
                return
        print("Barang tidak ditemukan.")
            
    def tampilkan_semua_barang(self):
        for barang in self.daftar_barang:
            print(barang.info())



class LogistikManager:
    def __init__(self, gudang):
        self.gudang = gudang
        self.riwayat_transaksi = []

    def beli_barang(self, supplier, barang, jumlah, tanggal):
        transaksi = TransaksiPembelian(supplier, barang, jumlah, tanggal)
        transaksi.proses()
        self.riwayat_transaksi.append(transaksi)
        print("Transaksi berhasil diproses.")

    def tampilkan_riwayat(self):
        for trx in self.riwayat_transaksi:
            print(trx.info())



g = Gudang()


