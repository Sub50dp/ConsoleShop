from django.db import models

from shop.models import Product
from users.models import CustomUser


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['create_date']

    def __str__(self):
        return f"Cart {self.pk} | {self.user} | {self.update_date}"

    def count_items(self):
        return self.cartitem_set.aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0

    def total_price(self):
        return sum(item.sum_total() for item in self.cartitem_set.all())


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def sum_total(self):
        return round(self.product.price * self.quantity, 2)

    def __str__(self):
        return f"{self.product}:{self.quantity}"
