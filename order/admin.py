from django.contrib import admin

from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "create_date", "status"]
    list_filter = ("status",)
    fields = ['user', 'full_name', 'status', 'phone_number', 'shipping_address', 'shipping_type',
              'comment',  'count_items', 'total_price', 'create_date', 'session_key']
    readonly_fields = ['create_date', 'count_items', 'total_price', 'session_key']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'quantity', 'sum_total']
    fields = ['product', 'order', 'quantity', 'sum_total']
    readonly_fields = ['sum_total']