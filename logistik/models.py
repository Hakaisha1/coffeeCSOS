from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine

# Base class untuk semua model
Base = declarative_base()

class Barang(Base):
    __tablename__ = 'barang'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String, nullable=False, unique=True)
    stok = Column(Integer, default=0)
    harga = Column(Integer, nullable=False)
    kadaluarsa = Column(String, nullable=True) # Bisa diganti tipe Date jika ingin format tanggal strict

    # Relasi ke transaksi (Opsional, agar bisa melihat history transaksi barang ini)
    transaksi = relationship("TransaksiPembelian", back_populates="barang")

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
        exp = self.kadaluarsa if self.kadaluarsa else "Tidak ada"
        return (
            f"Nama: {self.nama} | Stok: {self.stok} | Harga: {self.harga} | "
            f"Kadaluarsa: {exp}"
        )

    def __repr__(self):
        return f"<Barang(nama='{self.nama}', stok={self.stok})>"


class Supplier(Base):
    __tablename__ = 'supplier'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String, nullable=False)
    kontak = Column(String, nullable=True)

    # Relasi agar bisa melihat transaksi apa saja dari supplier ini
    transaksi = relationship("TransaksiPembelian", back_populates="supplier")

    def info(self):
        return f"Supplier: {self.nama} | Kontak: {self.kontak}"

    def __repr__(self):
        return f"<Supplier(nama='{self.nama}')>"


class TransaksiPembelian(Base):
    __tablename__ = 'transaksi_pembelian'

    id = Column(Integer, primary_key=True, autoincrement=True)
    jumlah = Column(Integer, nullable=False)
    tanggal = Column(String, nullable=False) # Bisa diganti tipe Date/DateTime
    
    # Foreign Keys (Menghubungkan tabel)
    supplier_id = Column(Integer, ForeignKey('supplier.id'))
    barang_id = Column(Integer, ForeignKey('barang.id'))

    # Relasi object
    supplier = relationship("Supplier", back_populates="transaksi")
    barang = relationship("Barang", back_populates="transaksi")

    def proses(self):
        """Menambahkan stok ke object barang yang terhubung"""
        if self.barang:
            self.barang.tambah_stok(self.jumlah)

    def info(self):
        nama_brg = self.barang.nama if self.barang else "Unknown"
        nama_supp = self.supplier.nama if self.supplier else "Unknown"
        return (
            f"Transaksi Pembelian: {self.jumlah} {nama_brg} "
            f"dari {nama_supp} pada {self.tanggal}"
        )

# Fungsi helper untuk membuat database dan tabel secara otomatis
def init_db(db_url='sqlite:///logistik_kopi.db'):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine