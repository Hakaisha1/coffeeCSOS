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

from pegawai.models import Pegawai, Barista, Waiter, Cleaner
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
        # Ambil semua tipe pegawai
        pegawai_list = Pegawai.objects.all()
        barista_list = Barista.objects.all()
        waiter_list = Waiter.objects.all()
        cleaner_list = Cleaner.objects.all()
        
        if not (pegawai_list.exists() or barista_list.exists() or waiter_list.exists() or cleaner_list.exists()):
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
                'jumlah_jam': 0,
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
            bonus = float(bar.bonus_per_jam) * bar.jumlah_jam
            total_gaji = gaji_pokok + bonus
            performance = (bar.jumlah_jam * 10) + (bar.jam_kerja * 5)

            employee_data = {
                'id_pegawai': bar.id_pegawai,
                'nama': bar.nama,
                'posisi': 'Barista',
                'shift': bar.shift,
                'jam_kerja': bar.jam_kerja,
                'jumlah_jam': bar.jumlah_jam,
                'gaji_pokok': gaji_pokok,
                'bonus': bonus,
                'total_gaji': total_gaji,
                'performance_score': performance,
                'jenis': 'barista'
            }
            self.employee_stats.append(employee_data)
        
        # Process Waiter
        for waiter in waiter_list:
            gaji_pokok = float(waiter.gaji_per_jam) * waiter.jam_kerja
            bonus = float(waiter.bonus_per_jam) * waiter.jumlah_jam
            total_gaji = gaji_pokok + bonus
            performance = (waiter.jumlah_jam * 10) + (waiter.jam_kerja * 5)

            employee_data = {
                'id_pegawai': waiter.id_pegawai,
                'nama': waiter.nama,
                'posisi': 'Waiter',
                'shift': waiter.shift,
                'jam_kerja': waiter.jam_kerja,
                'jumlah_jam': waiter.jumlah_jam,
                'gaji_pokok': gaji_pokok,
                'bonus': bonus,
                'total_gaji': total_gaji,
                'performance_score': performance,
                'jenis': 'waiter'
            }
            self.employee_stats.append(employee_data)
        
        # Process Cleaner
        for cleaner in cleaner_list:
            gaji_pokok = float(cleaner.gaji_per_jam) * cleaner.jam_kerja
            bonus = float(cleaner.bonus_per_jam) * cleaner.jumlah_jam
            total_gaji = gaji_pokok + bonus
            performance = (cleaner.jumlah_jam * 10) + (cleaner.jam_kerja * 5)

            employee_data = {
                'id_pegawai': cleaner.id_pegawai,
                'nama': cleaner.nama,
                'posisi': 'Cleaner',
                'shift': cleaner.shift,
                'jam_kerja': cleaner.jam_kerja,
                'jumlah_jam': cleaner.jumlah_jam,
                'gaji_pokok': gaji_pokok,
                'bonus': bonus,
                'total_gaji': total_gaji,
                'performance_score': performance,
                'jenis': 'cleaner'
            }
            self.employee_stats.append(employee_data)
        
        # Sort by performance
        self.employee_stats.sort(key=lambda x: x['performance_score'], reverse=True)
        self.best_employee = self.employee_stats[0] if self.employee_stats else None

        # Calculate aggregates
        total_jam_lembur = sum(stat['jumlah_jam'] for stat in self.employee_stats)
        total_jam_kerja = sum(stat['jam_kerja'] for stat in self.employee_stats)
        total_gaji = sum(stat['total_gaji'] for stat in self.employee_stats)
        total_bonus_lembur = sum(stat['bonus'] for stat in self.employee_stats)
        
        self.content = {
            'total_pegawai': len(self.employee_stats),
            'total_jumlah_jam': total_jam_lembur,  # Total jam lembur semua pegawai
            'total_jam_kerja': total_jam_kerja,    # Total jam kerja normal
            'total_gaji_dibayarkan': f"Rp {total_gaji:,.0f}",
            'total_bonus_lembur': f"Rp {total_bonus_lembur:,.0f}",
            'rata_rata_jumlah_jam': total_jam_lembur / len(self.employee_stats) if len(self.employee_stats) > 0 else 0,
            'pegawai_terbaik': {
                'id_pegawai': self.best_employee['id_pegawai'],
                'nama': self.best_employee['nama'],
                'posisi': self.best_employee['posisi'],
                'jumlah_jam': self.best_employee['jumlah_jam'],
                'performance_score': self.best_employee['performance_score']
            } if self.best_employee else None,
            'detail_pegawai': [
                {
                    'id_pegawai': emp['id_pegawai'],
                    'nama': emp['nama'],
                    'posisi': emp['posisi'],
                    'shift': emp['shift'],
                    'jam_kerja': emp['jam_kerja'],
                    'jumlah_jam': emp['jumlah_jam'],
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
        from customer.models import Member
        
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
            
            total_pembelian = riwayat_pembelian.aggregate(
                total=Sum('total_belanja')
            )['total'] or 0
            
            jumlah_transaksi = riwayat_pembelian.count()
            
            # Cek apakah customer adalah member
            is_member = Member.objects.filter(nama__iexact=cust.nama).exists()
            member_point = 0
            if is_member:
                member_obj = Member.objects.filter(nama__iexact=cust.nama).first()
                member_point = member_obj.point if member_obj else 0
            
            customer_data = {
                'nama': cust.nama,
                'total_pembelian': total_pembelian,
                'jumlah_transaksi': jumlah_transaksi,
                'is_member': is_member,
                'member_point': member_point,
            }
            
            customer_stats.append(customer_data)
        
        # Sort by total pembelian
        customer_stats.sort(key=lambda x: x['total_pembelian'], reverse=True)
        customer_terbaik = customer_stats[0] if customer_stats else None
        
        # Hitung total pembelian semua customer
        total_pembelian_semua = sum(stat['total_pembelian'] for stat in customer_stats)
        
        self.content = {
            'total_customer': len(customers),
            'total_pembelian_semua': f"Rp {total_pembelian_semua:,}",
            'rata_rata_pembelian': f"Rp {total_pembelian_semua / len(customers):,.0f}" if len(customers) > 0 else "Rp 0",
            'customer_terbaik': {
                'nama': customer_terbaik['nama'],
                'total_pembelian': f"Rp {customer_terbaik['total_pembelian']:,}",
                'jumlah_transaksi': customer_terbaik['jumlah_transaksi'],
                'is_member': customer_terbaik['is_member'],
                'member_point': customer_terbaik['member_point']
            } if customer_terbaik else None,
            'detail_customer': [
                {
                    'nama': cust['nama'],
                    'total_pembelian': f"Rp {cust['total_pembelian']:,}",
                    'jumlah_transaksi': cust['jumlah_transaksi'],
                    'is_member': cust['is_member'],
                    'member_point': cust['member_point']
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
    """Laporan Inventory/Logistik"""
    def __init__(self):
        super().__init__("Laporan Inventory")

    def generate(self):
        """Generate laporan inventory dari database logistik"""
        # Import models logistik
        from logistik.models import Barang, Supplier
        from datetime import date, timedelta
        
        barang_list = Barang.objects.all()
        supplier_list = Supplier.objects.all()
        
        if not barang_list.exists():
            self.content = {
                'message': 'Tidak ada data barang di inventory',
                'total_barang': 0,
                'total_stok': 0,
                'total_nilai_inventory': 'Rp 0',
                'detail_barang': [],
                'barang_hampir_habis': [],
                'barang_kadaluarsa': [],
                'supplier_list': []
            }
            return self.content
        
        # Analisis barang
        barang_stats = []
        total_nilai = 0
        barang_hampir_habis = []
        barang_kadaluarsa = []
        
        # Threshold untuk warning
        STOK_MINIMUM = 10
        HARI_KADALUARSA_WARNING = 30
        today = date.today()
        
        for barang in barang_list:
            nilai_total = barang.stok * barang.harga
            total_nilai += nilai_total
            
            # Cek status
            status = 'Normal'
            warnings = []
            
            # Cek stok rendah
            if barang.stok < STOK_MINIMUM:
                status = 'Stok Rendah'
                warnings.append('Stok hampir habis')
                barang_hampir_habis.append({
                    'nama': barang.nama,
                    'stok': barang.stok,
                    'minimum': STOK_MINIMUM
                })
            
            # Cek kadaluarsa
            hari_sampai_kadaluarsa = None
            if barang.kadaluarsa:
                hari_sampai_kadaluarsa = (barang.kadaluarsa - today).days
                if hari_sampai_kadaluarsa <= 0:
                    status = 'Kadaluarsa'
                    warnings.append('Sudah kadaluarsa')
                    barang_kadaluarsa.append({
                        'nama': barang.nama,
                        'kadaluarsa': barang.kadaluarsa.strftime('%Y-%m-%d'),
                        'hari': hari_sampai_kadaluarsa
                    })
                elif hari_sampai_kadaluarsa <= HARI_KADALUARSA_WARNING:
                    if status == 'Normal':
                        status = 'Hampir Kadaluarsa'
                    warnings.append(f'Kadaluarsa dalam {hari_sampai_kadaluarsa} hari')
                    barang_kadaluarsa.append({
                        'nama': barang.nama,
                        'kadaluarsa': barang.kadaluarsa.strftime('%Y-%m-%d'),
                        'hari': hari_sampai_kadaluarsa
                    })
            
            barang_data = {
                'id': barang.id,
                'nama': barang.nama,
                'stok': barang.stok,
                'harga': barang.harga,
                'nilai_total': nilai_total,
                'kadaluarsa': barang.kadaluarsa.strftime('%Y-%m-%d') if barang.kadaluarsa else 'N/A',
                'hari_sampai_kadaluarsa': hari_sampai_kadaluarsa,
                'status': status,
                'warnings': warnings
            }
            barang_stats.append(barang_data)
        
        # Sort by nilai total (descending)
        barang_stats.sort(key=lambda x: x['nilai_total'], reverse=True)
        
        # Barang dengan nilai tertinggi
        barang_nilai_tertinggi = barang_stats[0] if barang_stats else None
        
        # Supplier list
        supplier_data = [
            {
                'id': sup.id,
                'nama': sup.nama,
                'kontak': sup.kontak
            }
            for sup in supplier_list
        ]
        
        self.content = {
            'total_barang': len(barang_stats),
            'total_stok': sum(b['stok'] for b in barang_stats),
            'total_nilai_inventory': f"Rp {total_nilai:,}",
            'barang_nilai_tertinggi': {
                'nama': barang_nilai_tertinggi['nama'],
                'stok': barang_nilai_tertinggi['stok'],
                'nilai_total': f"Rp {barang_nilai_tertinggi['nilai_total']:,}"
            } if barang_nilai_tertinggi else None,
            'warning_summary': {
                'barang_stok_rendah': len(barang_hampir_habis),
                'barang_hampir_kadaluarsa': len([b for b in barang_kadaluarsa if b['hari'] > 0]),
                'barang_sudah_kadaluarsa': len([b for b in barang_kadaluarsa if b['hari'] <= 0])
            },
            'detail_barang': [
                {
                    'nama': b['nama'],
                    'stok': b['stok'],
                    'harga': f"Rp {b['harga']:,}",
                    'nilai_total': f"Rp {b['nilai_total']:,}",
                    'kadaluarsa': b['kadaluarsa'],
                    'status': b['status'],
                    'warnings': ', '.join(b['warnings']) if b['warnings'] else '-'
                }
                for b in barang_stats
            ],
            'barang_hampir_habis': barang_hampir_habis,
            'barang_kadaluarsa': sorted(barang_kadaluarsa, key=lambda x: x['hari']),
            'total_supplier': len(supplier_data),
            'supplier_list': supplier_data
        }
        
        return self.content
        

class FeedbackReport(Report):
    """Laporan Feedback Pelanggan"""
    def __init__(self):
        super().__init__("Laporan Feedback")

    def generate(self):
        """Generate laporan feedback dari database"""
        from feedback.models import Feedback
        
        feedbacks = Feedback.objects.all()
        
        if not feedbacks.exists():
            self.content = {
                'message': 'Belum ada feedback dari pelanggan',
                'total_feedback': 0
            }
            return self.content
        
        # Aggregate statistics
        total_feedback = feedbacks.count()
        
        # Rating statistics
        rating_counts = {}
        for i in range(1, 6):
            rating_counts[i] = feedbacks.filter(rating=i).count()
        
        # Calculate average rating
        total_rating_sum = sum(fb.rating for fb in feedbacks)
        rata_rata_rating = total_rating_sum / total_feedback if total_feedback > 0 else 0
        
        # Category breakdown
        kategori_counts = {}
        for value, label in Feedback.KATEGORI_CHOICES:
            kategori_counts[label] = feedbacks.filter(kategori=value).count()
        
        # Age group breakdown (jika ada umur)
        umur_counts = {}
        for value, label in Feedback.UMUR_CHOICES:
            umur_counts[label] = feedbacks.filter(umur=value).count()
        
        # Get recent feedbacks (latest 10)
        recent_feedbacks = feedbacks[:10]
        
        self.content = {
            'total_feedback': total_feedback,
            'rata_rata_rating': round(rata_rata_rating, 2),
            'rating_breakdown': rating_counts,
            'kategori_breakdown': kategori_counts,
            'umur_breakdown': umur_counts,
            'feedback_belum_dibaca': feedbacks.filter(is_read=False).count(),
            'feedback_sudah_dibaca': feedbacks.filter(is_read=True).count(),
            'recent_feedbacks': [
                {
                    'id': fb.id,
                    'nama': fb.nama or 'Anonim',
                    'rating': fb.rating,
                    'kategori': fb.get_kategori_display(),
                    'umur': fb.get_umur_display() if fb.umur else '-',
                    'komentar': fb.komentar,
                    'created_at': fb.created_at.strftime('%d %b %Y %H:%M'),
                    'is_read': fb.is_read
                }
                for fb in recent_feedbacks
            ]
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

        feedback_report = FeedbackReport()
        feedback_report.generate()
        self.reports.append(feedback_report)

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
            'feedback': FeedbackReport,
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


# # === MAIN EXECUTION (untuk testing) ===
# if __name__ == '__main__':
#     print("="*60)
#     print("COFFEE SHOP REPORTING SYSTEM")
#     print("="*60)
    
#     manager = ReportManager()
    
#     try:
#         # Test Employee Report
#         print("\n1. EMPLOYEE REPORT")
#         print("-" * 60)
#         emp_report = manager.get_report('employee')
#         print(json.dumps(emp_report.content, indent=2, ensure_ascii=False))
        
#         # Test Customer Report
#         print("\n2. CUSTOMER REPORT")
#         print("-" * 60)
#         cust_report = manager.get_report('customer')
#         print(json.dumps(cust_report.content, indent=2, ensure_ascii=False))
        
#         # Test Sales Report
#         print("\n3. SALES REPORT")
#         print("-" * 60)
#         sales_report = manager.get_report('sales')
#         print(json.dumps(sales_report.content, indent=2, ensure_ascii=False))
        
#         # Export all to JSON
#         print("\n4. EXPORT TO JSON")
#         print("-" * 60)
#         result = manager.export_to_json('coffee_reports.json')
#         print(result)
        
#         # Quick access functions
#         print("\n5. QUICK ACCESS")
#         print("-" * 60)
#         print("Pegawai Terbaik:", manager.get_best_employee())
#         print("Customer Terbaik:", manager.get_top_customer())
#         print("Menu Terlaris:", manager.get_best_selling_menu())
        
#     except Exception as e:
#         print(f"Error: {e}")
#         import traceback
#         traceback.print_exc()
    
#     print("\n" + "="*60)
