# ☕ Coffee CSOS - Coffee Shop Operating System

Sistem manajemen coffee shop berbasis Django dengan 4 subsistem utama: Customer, Pegawai, Logistik, dan Report.

## 📋 Status Proyek

**Status Keseluruhan**: Core Logic Complete - Ready for Integration & Deployment

## 🏗️ Struktur Proyek

```
coffeeCSOS/
├── customer/       # Subsistem Customer & Transaksi
├── pegawai/        # Subsistem Pegawai & Penggajian
├── logistik/       # Subsistem Inventory & Supplier
├── report/         # Subsistem Reporting & Analytics
└── coffeeCSOS/     # Django Project Settings
```

---

## 📊 Progress Subsistem

### 1️⃣ SUBSISTEM CUSTOMER

**PIC Subsistem**: [Nama PIC]

**Core Logic Status**: ✅ **COMPLETE**

#### ✅ Sudah Dikerjakan:
- [x] Class `Database` dengan SQLite integration
- [x] Model Django (`Customer`, `MenuItem`, `Riwayat`)
- [x] Sistem saldo customer (top-up & spending)
- [x] Sistem pemesanan dengan multiple items
- [x] Tracking riwayat transaksi lengkap
- [x] Validasi saldo & stok
- [x] File core logic: `customer/customer.py` (258 lines)

#### 🚧 Yang Perlu Dikerjakan:

**PRIORITAS TINGGI:**
- [ ] Buat `views.py` untuk handle request/response
  - [ ] View untuk daftar customer
  - [ ] View untuk detail customer & saldo
  - [ ] View untuk top-up saldo
  - [ ] View untuk pemesanan/checkout
  - [ ] View untuk riwayat transaksi
- [ ] Buat `urls.py` untuk routing
- [ ] Register models di `admin.py`
- [ ] Buat migrations dan jalankan migrate
- [ ] Integrasi dengan subsistem Logistik (kurangi stok saat order)

**PRIORITAS SEDANG:**
- [ ] Buat templates HTML (list customer, form order, dll)
- [ ] Implementasi forms Django untuk input data
- [ ] Validasi form & error handling
- [ ] AJAX untuk dynamic ordering interface

**PRIORITAS RENDAH:**
- [ ] Export riwayat ke CSV/PDF
- [ ] Notifikasi saldo rendah
- [ ] Sistem loyalty points

**TESTING:**
- [ ] Unit tests untuk models
- [ ] Integration tests untuk views
- [ ] Test edge cases (saldo insufficient, dll)

---

### 2️⃣ SUBSISTEM PEGAWAI

**PIC Subsistem**: [Nama PIC]

**Core Logic Status**: ✅ **COMPLETE**

#### ✅ Sudah Dikerjakan:
- [x] Class `pegawai` dengan sistem penggajian
- [x] Class `barista` (inheritance) dengan bonus system
- [x] Model Django (`pegawai`, `barista`)
- [x] Hitung gaji berdasarkan jam kerja
- [x] Bonus per minuman untuk barista
- [x] Sistem shift management
- [x] File core logic: `pegawai/pegawai.py` (143 lines)

#### 🚧 Yang Perlu Dikerjakan:

**PRIORITAS TINGGI:**
- [ ] Buat `views.py` untuk CRUD pegawai
  - [ ] View list semua pegawai
  - [ ] View detail pegawai & performa
  - [ ] View tambah/edit pegawai
  - [ ] View input jam kerja
  - [ ] View hitung & bayar gaji
- [ ] Buat `urls.py` untuk routing
- [ ] Register models di `admin.py`
- [ ] Buat migrations dan jalankan migrate
- [ ] Fix typo di model: `miuman_terjual` → `minuman_terjual`

**PRIORITAS SEDANG:**
- [ ] Buat templates untuk management pegawai
- [ ] Form untuk absensi/clock in-out
- [ ] Dashboard performa pegawai
- [ ] Export payroll report

**PRIORITAS RENDAH:**
- [ ] Sistem schedule/roster shift
- [ ] Tracking break time
- [ ] Performance metrics & rating
- [ ] Integration dengan biometric/attendance device

**TESTING:**
- [ ] Test perhitungan gaji base
- [ ] Test perhitungan bonus barista
- [ ] Test edge cases (overtime, dll)

---

### 3️⃣ SUBSISTEM LOGISTIK

**PIC Subsistem**: [Nama PIC]

**Core Logic Status**: ✅ **COMPLETE**

#### ✅ Sudah Dikerjakan:
- [x] Class `Barang` untuk inventory management
- [x] Class `Supplier` untuk data pemasok
- [x] Class `TransaksiPembelian` untuk purchase order
- [x] Sistem tambah/kurangi stok
- [x] Tracking tanggal kadaluarsa
- [x] Warning stok tidak cukup
- [x] File core logic: `logistik/logistik.py` (225 lines)

#### 🚧 Yang Perlu Dikerjakan:

**PRIORITAS TINGGI:**
- [ ] Buat Model Django untuk `Barang`, `Supplier`, `TransaksiPembelian`
- [ ] Buat `views.py` untuk inventory management
  - [ ] View list inventory dengan stok real-time
  - [ ] View tambah/edit barang
  - [ ] View list supplier
  - [ ] View purchase order
  - [ ] View restocking
- [ ] Buat `urls.py` untuk routing
- [ ] Register models di `admin.py`
- [ ] Buat migrations dan jalankan migrate
- [ ] API endpoint untuk cek ketersediaan stok (dipakai customer subsistem)

**PRIORITAS SEDANG:**
- [ ] Templates untuk inventory dashboard
- [ ] Form untuk purchase order
- [ ] Alert untuk stok menipis (< threshold)
- [ ] Alert untuk barang mendekati kadaluarsa
- [ ] History transaksi pembelian

**PRIORITAS RENDAH:**
- [ ] Barcode scanning integration
- [ ] Auto-reorder saat stok di bawah minimum
- [ ] Supplier rating & evaluation
- [ ] Waste tracking untuk expired items

**TESTING:**
- [ ] Test stok increment/decrement
- [ ] Test validasi stok tidak cukup
- [ ] Test purchase order workflow

---

### 4️⃣ SUBSISTEM REPORT

**PIC Subsistem**: [Nama PIC]

**Core Logic Status**: ⚠️ **NOT STARTED**

#### ✅ Sudah Dikerjakan:
- [x] Django app sudah di-generate
- [x] Model skeleton ready

#### 🚧 Yang Perlu Dikerjakan:

**PRIORITAS TINGGI:**
- [ ] Design struktur Model untuk reporting
  - [ ] Model untuk laporan harian
  - [ ] Model untuk laporan bulanan
  - [ ] Model untuk summary metrics
- [ ] Buat `views.py` untuk generate reports
  - [ ] View sales report (dari customer subsistem)
  - [ ] View inventory report (dari logistik subsistem)
  - [ ] View payroll report (dari pegawai subsistem)
  - [ ] View profit/loss statement
- [ ] Buat `urls.py` untuk routing
- [ ] Register models di `admin.py`
- [ ] Query aggregation untuk metrics

**PRIORITAS SEDANG:**
- [ ] Templates untuk dashboard & visualisasi
- [ ] Chart integration (Chart.js / Plotly)
- [ ] Export reports ke PDF
- [ ] Export reports ke Excel
- [ ] Filter berdasarkan date range

**PRIORITAS RENDAH:**
- [ ] Real-time analytics dashboard
- [ ] Predictive analytics (sales forecasting)
- [ ] Custom report builder
- [ ] Email scheduled reports

**TESTING:**
- [ ] Test data aggregation accuracy
- [ ] Test report generation performance
- [ ] Test export functionality

---

## 🚀 Roadmap Menuju Deployment

### FASE 1: Integration (Week 1-2)
- [ ] Integrate semua apps ke Django settings
- [ ] Setup URL routing untuk semua subsistem
- [ ] Migrate semua database models
- [ ] Test integrasi antar subsistem

### FASE 2: Views & Templates (Week 3-4)
- [ ] Buat semua views untuk keempat subsistem
- [ ] Design templates dengan Bootstrap/Tailwind
- [ ] Implement forms & validations
- [ ] Setup static files & media handling

### FASE 3: Testing (Week 5)
- [ ] Unit testing semua subsistem
- [ ] Integration testing
- [ ] User acceptance testing (UAT)
- [ ] Bug fixing & refinement

### FASE 4: Security & Performance (Week 6)
- [ ] Setup environment variables (.env)
- [ ] Secure SECRET_KEY & sensitive data
- [ ] CSRF & authentication protection
- [ ] Query optimization
- [ ] Caching setup

### FASE 5: Deployment (Week 7)
- [ ] Setup production server (Heroku/Railway/VPS)
- [ ] Configure production database (PostgreSQL)
- [ ] Setup static files serving (WhiteNoise/S3)
- [ ] Domain & SSL setup
- [ ] Monitoring & logging

---

## 🛠️ Setup Development Environment

### Prerequisites
```bash
Python 3.8+
Django 5.2.8
SQLite3 (dev) / PostgreSQL (prod)
```

### Installation

1. **Clone repository**
```bash
git clone <repository-url>
cd coffeeCSOS
```

2. **Setup virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install django
# Atau jika ada requirements.txt:
# pip install -r requirements.txt
```

4. **Setup database**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser**
```bash
python manage.py createsuperuser
```

6. **Run development server**
```bash
python manage.py runserver
```

Access: `http://127.0.0.1:8000/`

---

## 📝 Workflow Kolaborasi

### Branch Strategy
- `main` - Production-ready code
- `dev` - Development branch
- `feature/customer` - Customer subsystem
- `feature/pegawai` - Pegawai subsystem
- `feature/logistik` - Logistik subsystem
- `feature/report` - Report subsystem

### Git Workflow
```bash
# 1. Buat branch baru dari dev
git checkout dev
git pull origin dev
git checkout -b feature/nama-fitur

# 2. Kerjakan fitur, commit regularly
git add .
git commit -m "feat: deskripsi fitur"

# 3. Push ke remote
git push origin feature/nama-fitur

# 4. Buat Pull Request ke dev branch
# 5. Code review & merge oleh team lead
```

### Commit Message Convention
- `feat:` - Fitur baru
- `fix:` - Bug fix
- `refactor:` - Refactoring code
- `docs:` - Update dokumentasi
- `test:` - Tambah/update tests
- `style:` - Formatting, typo

---

## 👥 Tim & Pembagian Tugas

| Subsistem | PIC | Status | Deadline |
|-----------|-----|--------|----------|
| Customer | [Nama] | Integration Ready | Week 2 |
| Pegawai | [Nama] | Integration Ready | Week 2 |
| Logistik | [Nama] | Integration Ready | Week 2 |
| Report | [Nama] | Development | Week 3 |
| Integration | [Nama] | Pending | Week 4 |
| Deployment | [Nama] | Pending | Week 7 |

---

## 📚 Resources & Documentation

### Django Documentation
- [Django Official Docs](https://docs.djangoproject.com/)
- [Django Models](https://docs.djangoproject.com/en/5.2/topics/db/models/)
- [Django Views](https://docs.djangoproject.com/en/5.2/topics/http/views/)
- [Django Templates](https://docs.djangoproject.com/en/5.2/topics/templates/)

### Project-Specific Docs
- Core Logic Documentation (lihat file `.py` di masing-masing app)
- API Documentation (akan dibuat)
- Database Schema (akan dibuat)

---

## 🐛 Known Issues & Bugs

1. **Pegawai Models**: Typo `miuman_terjual` harus `minuman_terjual`
2. **Settings**: SECRET_KEY masih hardcoded, perlu pindah ke .env
3. **INSTALLED_APPS**: Apps belum didaftarkan ke settings.py

---

## 📞 Kontak & Support

**Project Lead**: [Nama]
**Repository**: [GitHub URL]
**Communication**: [Discord/Slack/WhatsApp Group]

---

## ⚖️ License

[Tentukan license - MIT, Apache, etc]

---

**Last Updated**: November 27, 2025
**Version**: 0.1.0 (Pre-release)

---

## 🎯 Next Steps (IMMEDIATE)

### Untuk SEMUA PIC:
1. ✅ Pastikan `.gitignore` sudah ter-commit
2. 📝 Isi nama PIC di bagian subsistem masing-masing
3. 🔍 Review core logic yang sudah ada
4. 🚀 Mulai kerjakan checklist prioritas TINGGI
5. 💬 Update progress di daily standup

### Quick Start Development:
```bash
# 1. Update INSTALLED_APPS di settings.py
INSTALLED_APPS = [
    # ... default apps
    'customer',
    'pegawai',
    'logistik',
    'report',
]

# 2. Jalankan migrations
python manage.py makemigrations
python manage.py migrate

# 3. Mulai development
python manage.py runserver
```

**Mari kita wujudkan Coffee CSOS! ☕🚀**
