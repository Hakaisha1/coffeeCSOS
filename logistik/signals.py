from django.db.models.signals import post_save
from django.dispatch import receiver
from customer.models import PesananDetail, MenuItemBahan

@receiver(post_save, sender=PesananDetail)
def kurangi_bahan_otomatis(sender, instance, created, **kwargs):
    if created:
        menu = instance.menu
        jumlah = instance.jumlah
        
        bahan_list = MenuItemBahan.objects.filter(menu_item=menu)

        for b in bahan_list:
            b.kurangi_stok(jumlah)
