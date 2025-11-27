# Kode bagian logistik
import sqlite3

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
            return True
        else:
            print("Stok tidak cukup!")
            return False

    def info(self):
        kadaluarsa = self.kadaluarsa if self.kadaluarsa else "Tidak ada"
        return (
            f"Nama: {self.nama} | Stok: {self.stok} | Harga: {self.harga} | "
            f"Kadaluarsa: {kadaluarsa}"
        )


class Supplier:
    def __init__(self, nama, kontak):
        self.nama = nama
        self.kontak = kontak

    def info(self):
        return f"Supplier: {self.nama} | Kontak: {self.kontak}"


class TransaksiPembelian:
    def __init__(self, supplier, barang, jumlah, tanggal):
        self.supplier = supplier
        self.barang = barang
        self.jumlah = jumlah
        self.tanggal = tanggal

    def proses(self):
        self.barang.tambah_stok(self.jumlah)

    def info(self):
        return (
            f"Transaksi Pembelian: {self.jumlah} {self.barang.nama} "
            f"dari {self.supplier.nama} pada {self.tanggal}"
        )
    



class Gudang:
    def __init__(self, db_name=r"E:\ngoding\coffeemgds\logistic\logistik_kopi.db"):
        self.db_name = db_name
        self.connection = None
        self.connect()
        self.create_table()



    def connect(self):
        try:
            import os
            self.connection = sqlite3.connect(self.db_name)
            print("Koneksi SQLite berhasil!")
            print("Database yang dipakai:", os.path.abspath(self.db_name))
        except Exception as e:
            print(f"Error saat koneksi: {e}")


    def create_table(self):
        if self.connection is None:
            return
        
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS barang (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT NOT NULL UNIQUE,
                    stok INTEGER NOT NULL,
                    harga INTEGER NOT NULL,
                    kadaluarsa TEXT
                )
            """)
            self.connection.commit()
            print("Tabel barang sudah siap.")
        except Exception as e:
            print(f"Error membuat tabel: {e}")
        finally:
            cursor.close()

    def tambah_barang(self, barang):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO barang (nama, stok, harga, kadaluarsa) VALUES (?, ?, ?, ?)",
                (barang.nama, barang.stok, barang.harga, barang.kadaluarsa)
            )
            self.connection.commit()
            print(f"Barang '{barang.nama}' berhasil ditambahkan ke database.")
        except Exception as e:
            print(f"Error menambah barang: {e}")
        finally:
            cursor.close()

    def cari_barang(self, nama):
        hasil = []
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "SELECT * FROM barang WHERE nama LIKE ?",
                (f"%{nama}%",)
            )
            rows = cursor.fetchall()
            for row in rows:
                barang = Barang(row[1], row[2], row[3], row[4])
                hasil.append(barang)
        except Exception as e:
            print(f"Error mencari barang: {e}")
        finally:
            cursor.close()
        
        return hasil

    def hapus_barang(self, nama):
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM barang WHERE nama = ?", (nama,))
            self.connection.commit()
            if cursor.rowcount > 0:
                print(f"{nama} berhasil dihapus dari database.")
            else:
                print("Barang tidak ditemukan.")
        except Exception as e:
            print(f"Error menghapus barang: {e}")
        finally:
            cursor.close()

    def tampilkan_semua_barang(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM barang")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    barang = Barang(row[1], row[2], row[3], row[4])
                    print(barang.info())
            else:
                print("Tidak ada barang di database.")
        except Exception as e:
            print(f"Error menampilkan barang: {e}")
        finally:
            cursor.close()

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Koneksi SQLite ditutup.")



# Menu interaktif
if __name__ == "__main__":
    g = Gudang()
    try:
        while True:
            print("\n" + "="*50)
            print("SISTEM MANAJEMEN LOGISTIK KOPI")
            print("="*50)
            print("1. Tampilkan semua barang")
            print("2. Cari barang")
            print("3. Tambah barang baru")
            print("4. Hapus barang")
            print("5. Keluar")
            print("="*50)
            
            pilihan = input("Pilih menu (1-5): ").strip()
            
            if pilihan == "1":
                print("\n--- Daftar Barang ---")
                g.tampilkan_semua_barang()
                
            elif pilihan == "2":
                nama = input("Masukkan nama barang yang dicari: ").strip()
                hasil = g.cari_barang(nama)
                if hasil:
                    print(f"\nHasil pencarian untuk '{nama}':")
                    for barang in hasil:
                        print(barang.info())
                else:
                    print(f"Barang '{nama}' tidak ditemukan.")
                    
            elif pilihan == "3":
                nama = input("Nama barang: ").strip()
                stok = int(input("Stok: "))
                harga = int(input("Harga: "))
                kadaluarsa = input("Tanggal kadaluarsa (YYYY-MM-DD) atau kosongkan: ").strip()
                
                barang_baru = Barang(nama, stok, harga, kadaluarsa if kadaluarsa else None)
                g.tambah_barang(barang_baru)
                print(f"Barang '{nama}' berhasil ditambahkan!")
                
            elif pilihan == "4":
                nama = input("Masukkan nama barang yang akan dihapus: ").strip()
                g.hapus_barang(nama)
                
            elif pilihan == "5":
                print("\nTerima kasih! Program ditutup.")
                g.close_connection()
                break
                
            else:
                print("Pilihan tidak valid! Silakan coba lagi.")
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh pengguna.")
        g.close_connection()

