from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from shop.models import Product
from users.models import CustomUser


class Order(models.Model):

    STATUS_CHOICES = (('pending', 'Pending'), ('refunded', 'Refunded'), ('completed', 'Completed'))

    SHIPPING_TYPE_CHOICES = (('free', 'Free'), ('paid', 'Paid'))

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="pending")
    phone_number = PhoneNumberField(max_length=50, region="UA", blank=True, null=True)
    shipping_address = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    shipping_type = models.CharField(max_length=255, choices=SHIPPING_TYPE_CHOICES, blank=True, null=True)
    session_key = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Order {self.pk} | {self.status} | {self.create_date}"

    def count_items(self):
        return self.orderitem_set.aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0

    def total_price(self):
        return sum(item.sum_total() for item in self.orderitem_set.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.order} | {self.product} | {self.quantity}"

    def sum_total(self):
        return round(self.product.price * self.quantity, 2)


