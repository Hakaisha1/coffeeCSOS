# Kode bagian report
import json
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coffeeCSOS.settings')
django.setup()

from datetime import datetime
from typing import List, Dict
from collections import defaultdict
from decimal import Decimal

# Import models dari setiap subsistem
from pegawai.models import Pegawai, Barista
from customer.models import Customer, MenuItem, Riwayat
from django.db.models import Sum, Count, Q


class Report:
    """Base class untuk semua report"""
    def __init__(self, title):
        self.title = title
        self.content = {}
    
    def generate(self):
        """Override method ini di subclass"""
        raise NotImplementedError("Subclass harus implement method generate()")
    
    def to_dict(self):
        """Return report content sebagai dictionary"""
        return {
            'title': self.title,
            'content': self.content
        }


class EmployeeReport(Report):
    """Laporan Karyawan dan Performa"""
    def __init__(self):
        super().__init__("Laporan Karyawan")
        self.best_employee = None
        self.employee_stats = []

    def generate(self):
        """Generate laporan pegawai dari database"""
        # Ambil semua pegawai biasa
        pegawai_list = Pegawai.objects.all()
        # Ambil semua barista
        barista_list = Barista.objects.all()
        
        if not pegawai_list.exists() and not barista_list.exists():
            self.content = {'message': 'Tidak ada data karyawan'}
            return self.content
        
        self.employee_stats = []
        
        # Process Pegawai biasa
        for emp in pegawai_list:
            gaji_pokok = float(emp.gaji_per_jam) * emp.jam_kerja
            
            employee_data = {
                'id_pegawai': emp.id_pegawai,
                'nama': emp.nama,
                'posisi': emp.posisi,
                'shift': emp.shift,
                'jam_kerja': emp.jam_kerja,
                'minuman_terjual': 0,
                'gaji_pokok': gaji_pokok,
                'bonus': 0,
                'total_gaji': gaji_pokok,
                'performance_score': emp.jam_kerja * 5,
                'jenis': 'pegawai'
            }
            self.employee_stats.append(employee_data)
        
        # Process Barista
        for bar in barista_list:
            gaji_pokok = float(bar.gaji_per_jam) * bar.jam_kerja
            bonus = float(bar.bonus_per_minuman) * bar.minuman_terjual
            total_gaji = gaji_pokok + bonus
            performance = (bar.minuman_terjual * 10) + (bar.jam_kerja * 5)

            employee_data = {
                'id_pegawai': bar.id_pegawai,
                'nama': bar.nama,
                'posisi': 'Barista',
                'shift': bar.shift,
                'jam_kerja': bar.jam_kerja,
                'minuman_terjual': bar.minuman_terjual,
                'gaji_pokok': gaji_pokok,
                'bonus': bonus,
                'total_gaji': total_gaji,
                'performance_score': performance,
                'jenis': 'barista'
            }
            self.employee_stats.append(employee_data)
        
        # Sort by performance
        self.employee_stats.sort(key=lambda x: x['performance_score'], reverse=True)
        self.best_employee = self.employee_stats[0] if self.employee_stats else None

        # Calculate aggregates
        total_minuman = sum(stat['minuman_terjual'] for stat in self.employee_stats)
        total_jam = sum(stat['jam_kerja'] for stat in self.employee_stats)
        total_gaji = sum(stat['total_gaji'] for stat in self.employee_stats)
        
        self.content = {
            'total_pegawai': len(self.employee_stats),
            'total_minuman_terjual': total_minuman,
            'total_jam_kerja': total_jam,
            'total_gaji_dibayarkan': f"Rp {total_gaji:,.0f}",
            'rata_rata_minuman_per_pegawai': total_minuman / len(self.employee_stats) if len(self.employee_stats) > 0 else 0,
            'pegawai_terbaik': {
                'id_pegawai': self.best_employee['id_pegawai'],
                'nama': self.best_employee['nama'],
                'posisi': self.best_employee['posisi'],
                'minuman_terjual': self.best_employee['minuman_terjual'],
                'performance_score': self.best_employee['performance_score']
            } if self.best_employee else None,
            'detail_pegawai': [
                {
                    'id_pegawai': emp['id_pegawai'],
                    'nama': emp['nama'],
                    'posisi': emp['posisi'],
                    'shift': emp['shift'],
                    'jam_kerja': emp['jam_kerja'],
                    'minuman_terjual': emp['minuman_terjual'],
                    'gaji_pokok': f"Rp {emp['gaji_pokok']:,.0f}",
                    'bonus': f"Rp {emp['bonus']:,.0f}",
                    'total_gaji': f"Rp {emp['total_gaji']:,.0f}",
                    'performance_score': emp['performance_score'],
                    'jenis': emp['jenis']
                }
                for emp in self.employee_stats
            ]
        }

        return self.content


class CustomerReport(Report):
    """Laporan Customer dan Saldo"""
    def __init__(self):
        super().__init__("Laporan Pelanggan")

    def generate(self):
        """Generate laporan customer dari database"""
        customers = Customer.objects.all()
        
        if not customers.exists():
            self.content = {'message': 'Tidak ada data pelanggan'}
            return self.content
        
        customer_stats = []
        total_saldo_semua = 0
        
        for cust in customers:
            # Hitung total transaksi customer
            riwayat_pembelian = Riwayat.objects.filter(
                customer=cust, 
                jenis='pembelian'
            )
            riwayat_topup = Riwayat.objects.filter(
                customer=cust, 
                jenis='top up'
            )
            
            total_pembelian = riwayat_pembelian.aggregate(
                total=Sum('total_belanja')
            )['total'] or 0
            
            total_topup = riwayat_topup.aggregate(
                total=Sum('perubahan')
            )['total'] or 0
            
            jumlah_transaksi = riwayat_pembelian.count()
            
            customer_data = {
                'nama': cust.nama,
                'saldo_saat_ini': cust.saldo,
                'total_top_up': total_topup,
                'total_pembelian': total_pembelian,
                'jumlah_transaksi': jumlah_transaksi,
            }
            
            customer_stats.append(customer_data)
            total_saldo_semua += cust.saldo
        
        # Sort by total pembelian
        customer_stats.sort(key=lambda x: x['total_pembelian'], reverse=True)
        customer_terbaik = customer_stats[0] if customer_stats else None
        
        self.content = {
            'total_customer': len(customers),
            'total_saldo_semua_customer': f"Rp {total_saldo_semua:,}",
            'rata_rata_saldo': f"Rp {total_saldo_semua / len(customers):,.0f}" if len(customers) > 0 else "Rp 0",
            'customer_terbaik': {
                'nama': customer_terbaik['nama'],
                'total_pembelian': f"Rp {customer_terbaik['total_pembelian']:,}",
                'jumlah_transaksi': customer_terbaik['jumlah_transaksi']
            } if customer_terbaik else None,
            'detail_customer': [
                {
                    'nama': cust['nama'],
                    'saldo_saat_ini': f"Rp {cust['saldo_saat_ini']:,}",
                    'total_top_up': f"Rp {cust['total_top_up']:,}",
                    'total_pembelian': f"Rp {cust['total_pembelian']:,}",
                    'jumlah_transaksi': cust['jumlah_transaksi']
                }
                for cust in customer_stats
            ]
        }
        
        return self.content


class SalesReport(Report):
    """Laporan Penjualan dari Transaksi Customer"""
    def __init__(self):
        super().__init__("Laporan Penjualan")

    def generate(self):
        """Generate laporan penjualan dari riwayat transaksi"""
        # Ambil semua transaksi pembelian
        transaksi_pembelian = Riwayat.objects.filter(jenis='pembelian')
        
        if not transaksi_pembelian.exists():
            self.content = {'message': 'Tidak ada data penjualan'}
            return self.content
        
        # Aggregate data
        total_penjualan = transaksi_pembelian.aggregate(
            total=Sum('total_belanja'),
            count=Count('id')
        )
        
        # Get menu items
        menu_items = MenuItem.objects.all()
        
        # Analisis per item (dari pesanan JSON)
        item_sales = {}
        for item in menu_items:
            item_sales[item.nama] = {
                'jumlah': 0,
                'total': 0
            }
        
        # Parse pesanan dari JSON
        for transaksi in transaksi_pembelian:
            if transaksi.pesanan:
                # pesanan adalah list of dict dengan format: 
                # [{'menu': 'Espresso', 'jumlah': 2, 'subtotal': 40000}, ...]
                for item in transaksi.pesanan:
                    menu_nama = item.get('menu')
                    jumlah = item.get('jumlah', 0)
                    subtotal = item.get('subtotal', 0)
                    
                    if menu_nama in item_sales:
                        item_sales[menu_nama]['jumlah'] += jumlah
                        item_sales[menu_nama]['total'] += subtotal
        
        # Sort by total revenue
        sorted_items = sorted(
            item_sales.items(), 
            key=lambda x: x[1]['total'], 
            reverse=True
        )
        
        # Menu terlaris
        menu_terlaris = sorted_items[0] if sorted_items and sorted_items[0][1]['jumlah'] > 0 else None
        
        self.content = {
            'total_transaksi': total_penjualan['count'] or 0,
            'total_pendapatan': f"Rp {total_penjualan['total'] or 0:,}",
            'rata_rata_transaksi': f"Rp {(total_penjualan['total'] or 0) / (total_penjualan['count'] or 1):,.0f}",
            'menu_terlaris': {
                'nama': menu_terlaris[0],
                'jumlah_terjual': menu_terlaris[1]['jumlah'],
                'total_pendapatan': f"Rp {menu_terlaris[1]['total']:,}"
            } if menu_terlaris else None,
            'detail_per_menu': [
                {
                    'nama_menu': item[0],
                    'jumlah_terjual': item[1]['jumlah'],
                    'total_pendapatan': f"Rp {item[1]['total']:,}"
                }
                for item in sorted_items if item[1]['jumlah'] > 0
            ]
        }
        
        return self.content


class InventoryReport(Report):
    """Laporan Inventory/Logistik (placeholder - menunggu models logistik)"""
    def __init__(self):
        super().__init__("Laporan Inventory")

    def generate(self):
        """
        Generate laporan inventory
        NOTE: Saat ini logistik.models belum memiliki model Barang, Supplier, dll
        Hanya ada model pegawai/barista yang duplikat.
        Implement ini setelah logistik models dibuat.
        """
        self.content = {
            'message': 'Laporan inventory belum tersedia',
            'note': 'Menunggu implementasi model Barang, Supplier, TransaksiPembelian di app logistik'
        }
        return self.content
        

class ReportManager:
    """Manager untuk mengelola semua jenis report"""
    def __init__(self):
        self.reports = []

    def generate_all(self):
        """Generate semua report"""
        employee_report = EmployeeReport()
        employee_report.generate()
        self.reports.append(employee_report)

        customer_report = CustomerReport()
        customer_report.generate()
        self.reports.append(customer_report)

        sales_report = SalesReport()
        sales_report.generate()
        self.reports.append(sales_report)

        inventory_report = InventoryReport()
        inventory_report.generate()
        self.reports.append(inventory_report)

        return self.reports
    
    def get_report(self, report_type: str):
        """Get specific report by type"""
        report_map = {
            'employee': EmployeeReport,
            'pegawai': EmployeeReport,
            'karyawan': EmployeeReport,
            'customer': CustomerReport,
            'pelanggan': CustomerReport,
            'sales': SalesReport,
            'penjualan': SalesReport,
            'inventory': InventoryReport,
            'logistik': InventoryReport,
            'stok': InventoryReport,
        }
        
        report_class = report_map.get(report_type.lower())
        if report_class:
            report = report_class()
            report.generate()
            return report
        else:
            raise ValueError(f"Tipe laporan '{report_type}' tidak dikenali.")
        
    def get_best_employee(self):
        """Quick access untuk pegawai terbaik"""
        employee_report = EmployeeReport()
        employee_report.generate()
        return employee_report.best_employee
    
    def get_top_customer(self):
        """Quick access untuk customer terbaik"""
        customer_report = CustomerReport()
        content = customer_report.generate()
        return content.get('customer_terbaik')
    
    def get_best_selling_menu(self):
        """Quick access untuk menu terlaris"""
        sales_report = SalesReport()
        content = sales_report.generate()
        return content.get('menu_terlaris')
    
    def export_to_json(self, filename='report_output.json'):
        """Export semua report ke JSON file"""
        all_reports = self.generate_all()
        output = {
            'generated_at': datetime.now().isoformat(),
            'reports': [report.to_dict() for report in all_reports]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=4, ensure_ascii=False)
        
        return f"Report berhasil di-export ke {filename}"


# === MAIN EXECUTION (untuk testing) ===
if __name__ == '__main__':
    print("="*60)
    print("COFFEE SHOP REPORTING SYSTEM")
    print("="*60)
    
    manager = ReportManager()
    
    try:
        # Test Employee Report
        print("\n1. EMPLOYEE REPORT")
        print("-" * 60)
        emp_report = manager.get_report('employee')
        print(json.dumps(emp_report.content, indent=2, ensure_ascii=False))
        
        # Test Customer Report
        print("\n2. CUSTOMER REPORT")
        print("-" * 60)
        cust_report = manager.get_report('customer')
        print(json.dumps(cust_report.content, indent=2, ensure_ascii=False))
        
        # Test Sales Report
        print("\n3. SALES REPORT")
        print("-" * 60)
        sales_report = manager.get_report('sales')
        print(json.dumps(sales_report.content, indent=2, ensure_ascii=False))
        
        # Export all to JSON
        print("\n4. EXPORT TO JSON")
        print("-" * 60)
        result = manager.export_to_json('coffee_reports.json')
        print(result)
        
        # Quick access functions
        print("\n5. QUICK ACCESS")
        print("-" * 60)
        print("Pegawai Terbaik:", manager.get_best_employee())
        print("Customer Terbaik:", manager.get_top_customer())
        print("Menu Terlaris:", manager.get_best_selling_menu())
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
