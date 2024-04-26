from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cart, CartItem


@receiver(post_save, sender=CartItem)
def update_cart_update_date(sender, instance, **kwargs):
    cart = instance.cart
    from django.utils import timezone
    cart.update_date = timezone.now()
    cart.save()
