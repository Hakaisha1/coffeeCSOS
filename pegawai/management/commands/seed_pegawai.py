from pathlib import Path
import json

from django.core.management.base import BaseCommand
from pegawai.models import Pegawai, Barista, Waiter, Cleaner


class Command(BaseCommand):
    help = "Seed data pegawai, barista, waiter, cleaner"

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parents[4]  # ke root project
        json_path = base_dir / "assets" / "database" / "pegawai.json"

        # Hapus data lama (optional)
        Pegawai.objects.all().delete()
        Barista.objects.all().delete()
        Waiter.objects.all().delete()
        Cleaner.objects.all().delete()

        # 1. Seed dari JSON untuk barista (kalau file ada)
        if json_path.exists():
            self.stdout.write(self.style.WARNING(f"Load data dari {json_path}"))
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for row in data:
                if row.get("jenis") == "barista":
                    bar = Barista.objects.create(
                        id_pegawai=row["id_pegawai"],
                        nama=row["nama"],
                        shift=row["shift"],
                        gaji_per_jam=row["gaji_per_jam"],
                        bonus_per_jam=row.get("bonus_per_jam", 0),
                        jumlah_jam=row.get("jumlah_jam", 0),
                        jam_kerja=row.get("jam_kerja", 0),
                    )
                    Pegawai.objects.create(
                        id_pegawai=row["id_pegawai"],
                        nama=row["nama"],
                        posisi=row.get("posisi", "Barista"),
                        shift=row["shift"],
                        gaji_per_jam=row["gaji_per_jam"],
                        jam_kerja=row.get("jam_kerja", 0),
                        jenis="barista",
                    )
                    self.stdout.write(self.style.SUCCESS(f"Barista dibuat: {bar}"))

        Barista.objects.create(
            id_pegawai="B001",
            nama="Bahlil",
            shift="Siang, Sore, Malam",
            gaji_per_jam=10000,
            bonus_per_jam=5000,
            jumlah_jam=6,
            jam_kerja=18,
        )

        Waiter.objects.create(
            id_pegawai="W001",
            nama="Ana",
            shift="Siang",
            gaji_per_jam=10000,
            bonus_per_jam=5000,
            jumlah_jam=0,
            jam_kerja=4,
        )

        Cleaner.objects.create(
            id_pegawai="C001",
            nama="Budi",
            shift="Malam",
            gaji_per_jam=9000,
            bonus_per_jam=5000,
            jumlah_jam=6,
            jam_kerja=6,
        )

        self.stdout.write(self.style.SUCCESS("Seeding pegawai selesai."))