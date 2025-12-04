from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register custom User model dengan UserAdmin bawaan Django
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin untuk User model dengan field role
    """
    # Tampilkan kolom ini di list view
    list_display = ['username', 'email', 'role', 'first_name', 'last_name', 'is_staff', 'is_active']
    
    # Filter berdasarkan ini
    list_filter = ['role', 'is_staff', 'is_active', 'date_joined']
    
    # Bisa search berdasarkan ini
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    # Tambahkan field 'role' ke form edit user
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )
    
    # Tambahkan field 'role' ke form add user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )