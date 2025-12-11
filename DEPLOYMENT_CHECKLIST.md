# 🚀 Deployment Checklist untuk PythonAnywhere

## ❌ YANG HARUS DIPERBAIKI SEKARANG:

### 1. **Update .gitignore**
```gitignore
# Tambahkan ini ke .gitignore
fix_tables.py
.env
```

### 2. **Buat file .env untuk production secrets**
```bash
# File: .env (JANGAN commit ke Git!)
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
DATABASE_URL=sqlite:///db.sqlite3
```

### 3. **Update settings.py untuk production**
```python
import os
from pathlib import Path
from decouple import config  # pip install python-decouple

SECRET_KEY = config('SECRET_KEY', default='django-insecure-fallback')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')
```

### 4. **Update requirements.txt**
```bash
python-decouple==3.8
```

## ✅ YANG SUDAH BENAR:

- ✅ WhiteNoise sudah configured untuk static files
- ✅ Argon2 password hashing aktif
- ✅ STATIC_ROOT sudah di-set
- ✅ Migration files sudah lengkap (0001, 0002, 0003)
- ✅ AUTH_USER_MODEL sudah di-set
- ✅ LOGIN_URL dan redirect URLs sudah configured

## 📋 LANGKAH DEPLOYMENT KE PYTHONANYWHERE:

### A. Persiapan Lokal
```bash
# 1. Commit semua changes
git add .
git commit -m "Prepare for production deployment"
git push origin main

# 2. Test collectstatic
python manage.py collectstatic --noinput

# 3. Verify migrations
python manage.py showmigrations
```

### B. Di PythonAnywhere Console
```bash
# 1. Clone repository
git clone https://github.com/yourusername/coffeeCSOS.git
cd coffeeCSOS

# 2. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
echo "SECRET_KEY=your-new-secret-key" > .env
echo "DEBUG=False" >> .env
echo "ALLOWED_HOSTS=yourusername.pythonanywhere.com" >> .env

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Collect static files
python manage.py collectstatic --noinput
```

### C. Configure Web App di PythonAnywhere Dashboard

1. **Source code**: `/home/yourusername/coffeeCSOS`
2. **Working directory**: `/home/yourusername/coffeeCSOS`
3. **Virtualenv**: `/home/yourusername/coffeeCSOS/venv`
4. **WSGI configuration file**:
```python
import os
import sys

path = '/home/yourusername/coffeeCSOS'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'coffeeCSOS.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

5. **Static files mapping**:
   - URL: `/static/`
   - Directory: `/home/yourusername/coffeeCSOS/staticfiles/`

### D. Post-Deployment Verification

```bash
# Test URLs:
https://yourusername.pythonanywhere.com/
https://yourusername.pythonanywhere.com/login/
https://yourusername.pythonanywhere.com/dashboard/
https://yourusername.pythonanywhere.com/report/

# Check logs di PythonAnywhere:
# Dashboard -> Web -> Log files
# - Error log
# - Server log
```

## 🔒 SECURITY CHECKLIST:

- [ ] SECRET_KEY tidak hardcoded
- [ ] DEBUG = False di production
- [ ] ALLOWED_HOSTS hanya domain yang valid
- [ ] db.sqlite3 tidak di-commit
- [ ] .env tidak di-commit
- [ ] fix_tables.py sudah dihapus
- [ ] Argon2 password hasher aktif

## ⚠️ CATATAN PENTING:

1. **Database**: PythonAnywhere akan mulai dengan database kosher, jadi tidak perlu khawatir tentang masalah sinkronisasi yang terjadi di lokal
2. **Migration**: Jalankan migrations di PythonAnywhere akan membuat schema yang bersih
3. **Static Files**: Pastikan `collectstatic` berhasil sebelum reload web app
4. **Logs**: Selalu cek error log jika ada masalah

## 🎯 NEXT STEPS SETELAH DEPLOY:

1. Test semua fitur:
   - Login/Logout
   - Customer ordering
   - Report generation
   - Role-based access

2. Seed data (optional):
   ```bash
   python manage.py shell < quick_seed.py
   python manage.py shell < seed_inventory.py
   ```

3. Monitor performance dan logs

---

**Status Saat Ini**: ⚠️ BELUM SIAP DEPLOY
**Action Required**: Update settings.py, .gitignore, dan hapus file temporary
