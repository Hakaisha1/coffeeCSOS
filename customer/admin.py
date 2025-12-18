from django.contrib import admin
from .models import (
    MenuItem,
    Customer,
    Riwayat,
    Pesanan,
    PesananDetail,
    MenuItemBahan,
    Member,
    RatingMenu,
    RatingCoffeeshop
)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("nama", "harga")
    search_fields = ("nama",)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("nama",)
    search_fields = ("nama",)


@admin.register(Riwayat)
class RiwayatAdmin(admin.ModelAdmin):
    list_display = ("customer", "total_belanja", "timestamp")
    list_filter = ("timestamp",)
    search_fields = ("customer__nama",)


@admin.register(Pesanan)
class PesananAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "total_harga", "tanggal")
    list_filter = ("tanggal",)
    search_fields = ("customer__nama",)


@admin.register(PesananDetail)
class PesananDetailAdmin(admin.ModelAdmin):
    list_display = ("menu", "customer", "jumlah", "total_harga", "tanggal")
    list_filter = ("tanggal",)
    search_fields = ("menu__nama", "customer__nama")


@admin.register(MenuItemBahan)
class MenuItemBahanAdmin(admin.ModelAdmin):
    list_display = ("menu_item", "barang", "jumlah_dibutuhkan")
    search_fields = ("menu_item__nama", "barang__nama")


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("nama", "pekerjaan", "umur", "point")
    search_fields = ("nama", "pekerjaan")



