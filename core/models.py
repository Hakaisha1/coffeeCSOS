from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User model dengan role-based access control
    - EMPLOYEE: Akses customer, pegawai
    - INVENTORY_MANAGER: Akses customer, pegawai, logistik
    - GENERAL_MANAGER: Akses semua (termasuk report)
    """
    ROLE_CHOICES = [
        ('EMPLOYEE', 'Employee'),
        ('INVENTORY_MANAGER', 'Inventory Manager'),
        ('GENERAL_MANAGER', 'General Manager'),
    ]

    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='EMPLOYEE',
        help_text='Role menentukan akses ke app mana saja'
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

