from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .report import ReportManager, EmployeeReport, CustomerReport, SalesReport, InventoryReport
import json
from datetime import datetime

def report_dashboard(request):
    """Dashboard utama - menampilkan ringkasan semua report"""
    manager = ReportManager()
    
    try:
        all_reports = manager.generate_all()
        best_employee = manager.get_best_employee()
        top_customer = manager.get_top_customer()
        best_menu = manager.get_best_selling_menu()
        
        context = {
            'page_title': 'Dashboard Report',
            'best_employee': best_employee,
            'top_customer': top_customer,
            'best_menu': best_menu,
            'reports': all_reports,
            'generated_at': datetime.now()
        }
        
        return render(request, 'report/dashboard.html', context)
    
    except Exception as e:
        context = {
            'error': str(e),
            'page_title': 'Dashboard Report - Error'
        }
        return render(request, 'report/dashboard.html', context)


def employee_report_view(request):
    """Halaman laporan pegawai dengan detail lengkap"""
    manager = ReportManager()
    
    try:
        emp_report = manager.get_report('employee')
        
        context = {
            'page_title': 'Laporan Karyawan',
            'report': emp_report.content,
            'report_type': 'employee'
        }
        
        return render(request, 'report/employee_report.html', context)
    
    except Exception as e:
        context = {
            'error': str(e),
            'page_title': 'Laporan Karyawan - Error'
        }
        return render(request, 'report/employee_report.html', context)


def customer_report_view(request):
    """Halaman laporan pelanggan"""
    manager = ReportManager()

    try: 
        cust_report = manager.get_report('customer')

        context = {
            'page_title': 'Laporan Pelanggan',
            'report': cust_report.content,
            'report_type': 'customer'
        }

        return render(request, 'report/customer_report.html', context)
    
    except Exception as e:
        context = {
            'error': str(e),
            'page_title': 'Laporan Pelanggan - Error'
        }
        return render(request, 'report/customer_report.html', context)

def sales_report_view(request):
    """Halaman laporan penjualan"""
    manager = ReportManager()
    try:
        sales_report = manager.get_report('sales')

        context = {
            'page_title': 'Laporan Penjualan',
            'report': sales_report.content,
            'report_type': 'sales'
        }

        return render(request, 'report/sales_report.html', context)
    except Exception as e:
        context = {
            'error': str(e),
            'page_title': 'Laporan Penjualan - Error'
        }
        return render(request, 'report/sales_report.html', context)

def inventory_report_view(request):
    """Halaman laporan inventory"""
    pass


def api_employee_report(request):

    """API endpoint untuk data employee dalam format JSON"""
    manager = ReportManager()
    
    try:
        emp_report = manager.get_report('employee')
        return JsonResponse({
            'success': True,
            'data': emp_report.content
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


def api_customer_report(request):
    """API endpoint untuk data customer dalam format JSON"""
    manager = ReportManager()

    try:
        cust_report = manager.get_report('customer')
        return JsonResponse({
            'success': True,
            'data': cust_report.content
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


def api_sales_report(request):
    """API endpoint untuk data sales dalam format JSON"""
    manager = ReportManager()

    try:
        sales_report = manager.get_report('sales')
        return JsonResponse({
            'success': True,
            'data': sales_report.content
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


def export_all_reports_json(request):
    """Export semua report ke JSON file dan download"""
    manager = ReportManager()
    
    try:
        all_reports = manager.generate_all()
        output = {
            'generated_at': datetime.now().isoformat(),
            'reports': [report.to_dict() for report in all_reports]
        }
        
        response = HttpResponse(
            json.dumps(output, indent=2, ensure_ascii=False),
            content_type='application/json'
        )
        response['Content-Disposition'] = f'attachment; filename="coffee_reports_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json"'
        
        return response
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


def export_employee_report_csv(request):
    """Export employee report ke CSV file"""
    manager = ReportManager()

    try:
        emp_report = manager.get_report('employee')
        
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="employee_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'

        writer = csv.writer(response)
        if emp_report.content:
            headers = emp_report.content[0].keys()
            writer.writerow(headers)
            for row in emp_report.content:
                writer.writerow(row.values())
        
        return response

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


def quick_stats_api(request):
    """API untuk quick stats"""
    pass


def compare_reports(request):
    """View untuk membandingkan report periode berbeda"""
    pass
