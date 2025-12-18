from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama', 'rating', 'kategori', 'created_at', 'is_read']
    list_filter = ['rating', 'kategori', 'is_read', 'created_at']
    search_fields = ['nama', 'email', 'komentar']
    readonly_fields = ['created_at']
    list_editable = ['is_read']
    
    fieldsets = (
        ('Data Customer', {
            'fields': ('nama', 'email', 'nomor_meja')
        }),
        ('Feedback', {
            'fields': ('rating', 'kategori', 'komentar')
        }),
        ('Metadata', {
            'fields': ('created_at', 'is_read')
        }),
    )
