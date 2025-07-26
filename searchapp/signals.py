from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product
from .search_service import index_product, delete_product

@receiver(post_save, sender=Product)
def sync_product_to_es(sender, instance, **kwargs):
    index_product(instance)

@receiver(post_delete, sender=Product)
def remove_product_from_es(sender, instance, **kwargs):
    delete_product(instance.id)
