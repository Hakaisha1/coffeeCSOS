from django.urls import path
from . import views

app_name = 'report'

urlpatterns = [
    path('', views.report_dashboard, name='dashboard'),
    
    path('employee/', views.employee_report_view, name='employee_report'),
    path('customer/', views.customer_report_view, name='customer_report'),
    path('sales/', views.sales_report_view, name='sales_report'),
    path('inventory/', views.inventory_report_view, name='inventory_report'),
    path('feedback/', views.feedback_report_view, name='feedback_report'),
    
    path('api/employee/', views.api_employee_report, name='api_employee'),
    path('api/customer/', views.api_customer_report, name='api_customer'),
    path('api/sales/', views.api_sales_report, name='api_sales'),
    path('api/feedback/', views.api_feedback_report, name='api_feedback'),
    
    path('export/all/json/', views.export_all_reports_json, name='export_all_json'),
    path('export/employee/csv/', views.export_employee_report_csv, name='export_employee_csv'),
    
    path('api/quick-stats/', views.quick_stats_api, name='quick_stats'),
    path('compare/', views.compare_reports, name='compare_reports'),
]
