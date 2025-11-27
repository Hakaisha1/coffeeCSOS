# Kode bagian report
import json
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coffeemgds.settings')
django.setup()

from datetime import datetime
from typing import List, Dict
from collections import defaultdict
from pegawai.models import pegawai, barista
from logistik.models import Barang, Supplier, TransaksiPembelian
from customer.models import Pelanggan, TransaksiPenjualan


class Report:
    pass
    
class EmployeeReport(Report):
    def __init__(self):
        super().__init__("Laporan Karyawan")
        self.best_employee = None
        self.employee = []

    def generate(self):
        employees = pegawai.objects.all()
        if not employees.exists():
            self.content = {'message': 'Tidak ada data karyawan'}
            return self.content
        
        self.employee_stats = []
        for emp in employees:
            gaji_pokok = emp.gaji_per_jam * emp.jam_kerja
            
            if hasattr(emp, 'barista'):
                bonus = emp.barista.bonus_per_minuman * emp.barista.minuman_terjual
                minuman_terjual = emp.barista.miuman_terjual
            else:
                bonus = 0
                minuman_terjual = 0
            
            total_gaji = gaji_pokok + bonus
            performance = (minuman_terjual * 10) + (emp.jam_kerja * 5)

            employee_data = {
                'id_pegawai': emp.id_pegawai,
                'nama': emp.nama,
                'posisi': emp.posisi,
                'shift': emp.shift,
                'jam_kerja': emp.jam_kerja,
                'minuman_terjual': minuman_terjual,
                'gaji_pokok': f"Rp {gaji_pokok:,}",
                'bonus': f"Rp {bonus:,}",
                'total_gaji': f"Rp {total_gaji:,}",
                'performance_score': performance
            }

            self.employee_stats.append(employee_data)
        
        self.employee_stats.sort(key=lambda x: x['performance_score'], reverse=True)
        self.best_employee = self.employee_stats[0] if self.employee_stats else None

        total_minuman = sum(stat['minuman_terjual'] for stat in self.employee_stats)
        total_jam = sum(stat['jam_kerja'] for stat in self.employee_stats)
        
        self.content = {
            'total_pegawai': len(employees),
            'total_minuman_terjual': total_minuman,
            'total_jam_kerja': total_jam,
            'rata_rata_minuman_per_pegawai': total_minuman / len(employees) if len(employees) > 0 else 0,
            'pegawai_terbaik': {
                'nama' : self.best_employee['nama'],
                'minuman_terjual': self.best_employee['minuman_terjual'],
                'performance_score': self.best_employee['performance_score']
            } if self.best_employee else None,
            'detail_pegawai': self.employee_stats
        }

        return self.content
    
class InventoryReport(Report):
    pass

class CustomerReport(Report):
    def __init__(self):
        super().__init__("Laporan Pelanggan")

class SalesReport(Report):
    def __init__(self):
        super().__init__("Laporan Karyawan")
        

class ReportManager:
    def __init__(self):
        self.reports = []

    def generate_all(self):
        employees = EmployeeReport()
        employees.generate()
        self.reports.append(employees)

        inventory = InventoryReport()
        inventory.generate()
        self.reports.append(inventory)

        customer = CustomerReport()
        customer.generate()
        self.reports.append(customer)

        sales = SalesReport()
        sales.generate()
        self.reports.append(sales)
        return self.reports
    
    def get_report(self, report_type:str):
        report_map = {
            'employee': EmployeeReport,
            'inventory': InventoryReport,
            'customer': CustomerReport,
            'sales': SalesReport
        }
        report_class = report_map.get(report_type.lower())
        if report_class:
            report = report_class()
            report.generate()
            return report
        else:
            raise ValueError(f"Tipe laporan '{report_type}' tidak dikenali.")
        
    def get_best_employee(self):
        employee_report = EmployeeReport()
        employee_report.generate()
        return employee_report.best_employee
    

