# seed_menu_item_bahan.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coffeeCSOS.settings')  # ganti dengan nama projectmu
django.setup()

from customer.models import MenuItem, MenuItemBahan
from logistik.models import Barang

# =====================
# Data menu dan bahan
# =====================
menu_bahan = {
    "Espresso": ["Biji Kopi"],
    "Ice Cafe Latte": ["Biji Kopi", "Susu"],
    "Matcha Latte": ["Bubuk Matcha", "Susu", "Gula"],
    "Butterscotch Coffee": ["Biji Kopi", "Susu", "Sirup Butterscotch"]
}

# =====================
# Seed menu item bahan
# =====================
for menu_nama, bahan_list in menu_bahan.items():
    try:
        menu_item = MenuItem.objects.get(nama=menu_nama)
    except MenuItem.DoesNotExist:
        print(f"MenuItem '{menu_nama}' tidak ditemukan. Lewatkan.")
        continue

    for bahan_nama in bahan_list:
        try:
            barang = Barang.objects.get(nama=bahan_nama)
        except Barang.DoesNotExist:
            print(f"Barang '{bahan_nama}' tidak ditemukan. Lewatkan.")
            continue

        # default jumlah dibutuhkan = 1
        MenuItemBahan.objects.get_or_create(
            menu_item=menu_item,
            barang=barang,
            jumlah_dibutuhkan=1
        )

print("Seed MenuItemBahan selesai!")
