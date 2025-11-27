import sqlite3
import os


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("customer.db")
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        # Tabel customer
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer (
                nama TEXT PRIMARY KEY,
                saldo INTEGER DEFAULT 0
            )
        """)

        # Tabel riwayat top up & belanja
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS riwayat (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer TEXT,
                jenis TEXT,
                saldo_awal INTEGER,
                perubahan INTEGER,
                total_belanja INTEGER,
                saldo_akhir INTEGER
            )
        """)

        # Tabel detail pesanan (jika jenis = pembelian)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pesanan_detail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                riwayat_id INTEGER,
                menu TEXT,
                jumlah INTEGER,
                subtotal INTEGER
            )
        """)

        self.conn.commit()

    def close(self):
        self.conn.close()


db = Database()


class MenuItem:
    def __init__(self, nama, harga):
        self.nama = nama
        self.harga = harga

    def __str__(self):
        return f"{self.nama} - Rp{self.harga:,}"


class Pesanan:
    def __init__(self, customer):
        self.customer = customer
        self.daftar_pesanan = []
        self.total = 0

    def tambah_item(self, item, jumlah):
        subtotal = item.harga * jumlah
        self.daftar_pesanan.append((item, jumlah, subtotal))
        self.total += subtotal

    def tampilkan(self):
        print("\n=== Detail Pesanan ===")
        for item, jumlah, subtotal in self.daftar_pesanan:
            print(f"{item.nama} (x{jumlah}) = Rp{subtotal:,}")
        print(f"Total: Rp{self.total:,}")


class Customer:
    def __init__(self, nama):
        self.nama = nama

        # Cek apakah customer sudah ada
        db.cursor.execute("SELECT saldo FROM customer WHERE nama=?", (nama,))
        data = db.cursor.fetchone()

        if data is None:
            # customer baru → buat record
            db.cursor.execute("INSERT INTO customer (nama, saldo) VALUES (?, ?)", (nama, 0))
            db.conn.commit()
            self.saldo = 0
        else:
            self.saldo = data[0]


    def update_saldo(self, jumlah):
        self.saldo = jumlah
        db.cursor.execute("UPDATE customer SET saldo=? WHERE nama=?", (self.saldo, self.nama))
        db.conn.commit()


    def top_up(self):
        print(f"\nSaldo Anda sekarang: Rp{self.saldo:,}")
        try:
            jumlah = int(input("Masukkan jumlah top up: Rp"))
            if jumlah <= 0:
                print("Jumlah tidak boleh 0.")
                return

            saldo_awal = self.saldo
            saldo_akhir = saldo_awal + jumlah

            # simpan
            db.cursor.execute("""
                INSERT INTO riwayat (customer, jenis, saldo_awal, perubahan, saldo_akhir)
                VALUES (?, ?, ?, ?, ?)
            """, (self.nama, "top up", saldo_awal, jumlah, saldo_akhir))
            db.conn.commit()

            self.update_saldo(saldo_akhir)

            print(f"Top up berhasil! Saldo sekarang: Rp{self.saldo:,}")

        except ValueError:
            print("Masukkan angka valid.")


    def bayar(self, total, daftar_pesanan):
        if self.saldo < total:
            return False

        saldo_awal = self.saldo
        saldo_akhir = saldo_awal - total

        # Simpan ke riwayat (jenis pembelian)
        db.cursor.execute("""
            INSERT INTO riwayat (customer, jenis, saldo_awal, total_belanja, saldo_akhir)
            VALUES (?, ?, ?, ?, ?)
        """, (self.nama, "pembelian", saldo_awal, total, saldo_akhir))
        riwayat_id = db.cursor.lastrowid

        # Simpan detail pesanan
        for item, jumlah, subtotal in daftar_pesanan:
            db.cursor.execute("""
                INSERT INTO pesanan_detail (riwayat_id, menu, jumlah, subtotal)
                VALUES (?, ?, ?, ?)
            """, (riwayat_id, item.nama, jumlah, subtotal))

        db.conn.commit()

        # Update saldo customer
        self.update_saldo(saldo_akhir)

        print("\nPembayaran berhasil!")
        print(f"Sisa saldo: Rp{self.saldo:,}")
        return True


    def lihat_riwayat(self):
        print("\n=== RIWAYAT TRANSAKSI ===")

        db.cursor.execute("SELECT * FROM riwayat WHERE customer=?", (self.nama,))
        data = db.cursor.fetchall()

        if not data:
            print("Belum ada riwayat.")
            return

        for i, r in enumerate(data, 1):
            (id_, customer, jenis, saldo_awal, perubahan,
             total_belanja, saldo_akhir) = r

            print(f"\n--- Transaksi {i} ---")
            print(f"Jenis        : {jenis}")
            print(f"Saldo Awal   : Rp{saldo_awal:,}")

            if jenis == "top up":
                print(f"Top Up       : Rp{(perubahan or 0):,}")
            else:
                print(f"Total Belanja: Rp{(total_belanja or 0):,}")

                # Detail pesanan
                print("Detail Pesanan:")
                db.cursor.execute("SELECT menu, jumlah, subtotal FROM pesanan_detail WHERE riwayat_id=?", (id_,))
                items = db.cursor.fetchall()
                for m, j, s in items:
                    print(f" - {m} x{j} = Rp{s:,}")

            print(f"Saldo Akhir  : Rp{saldo_akhir:,}")


    def buat_pesanan(self, menu):
        pesanan = Pesanan(self)

        print("\n=== MENU ===")
        for i, item in enumerate(menu, 1):
            print(f"{i}. {item}")

        while True:
            try:
                pilih = int(input("\nPilih menu (0 untuk selesai): "))
                if pilih == 0:
                    break
                if 1 <= pilih <= len(menu):
                    jumlah = int(input("Jumlah: "))
                    pesanan.tambah_item(menu[pilih - 1], jumlah)
                    print("Ditambahkan!")
            except:
                print("Input tidak valid.")

        if not pesanan.daftar_pesanan:
            print("Tidak ada pesanan.")
            return

        pesanan.tampilkan()

        if self.bayar(pesanan.total, pesanan.daftar_pesanan):
            print("\n=== STRUK ===")
            for item, jumlah, subtotal in pesanan.daftar_pesanan:
                print(f"{item.nama} x{jumlah} = Rp{subtotal:,}")
            print(f"TOTAL = Rp{pesanan.total:,}")



if __name__ == "__main__":
    menu = [
        MenuItem("Espresso", 20000),
        MenuItem("Ice Cafe Latte", 25000),
        MenuItem("Cappuccino", 23000),
        MenuItem("Matcha Latte", 27500),
        MenuItem("Butterscotch Coffee", 32000)
    ]

    nama = input("Masukkan nama customer: ")
    cust = Customer(nama)

    while True:
        print("\n=== MENU UTAMA ===")
        print("1. Buat Pesanan")
        print("2. Lihat Riwayat")
        print("3. Top Up")
        print("0. Keluar")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            cust.buat_pesanan(menu)
        elif pilih == "2":
            cust.lihat_riwayat()
        elif pilih == "3":
            cust.top_up()
        elif pilih == "0":
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid.")
