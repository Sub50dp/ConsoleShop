from django.contrib import admin

from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'count_items', 'total_price', 'create_date', 'update_date']
    fields = ['user', 'count_items', 'total_price', 'create_date', 'update_date', 'session_key']
    readonly_fields = ['create_date', 'update_date', 'session_key', 'count_items', 'total_price']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'quantity', 'sum_total']
    fields = ['product', 'cart', 'quantity', 'sum_total']
    readonly_fields = ['sum_total']