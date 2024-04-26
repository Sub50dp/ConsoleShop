from rest_framework import serializers

from cart.models import CartItem, Cart
from shop.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Cart
        fields = ['id', 'user', 'count_items', 'total_price', 'create_date', 'update_date']
        only_read = ['user', 'count_items', 'total_price', 'create_date', 'update_date']


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'sum_total']

    def to_representation(self, instance):
        data = ProductSerializer(instance.product).data
        data['id'] = instance.id
        data['quantity'] = instance.quantity
        data['sum_total'] = instance.sum_total()
        return data


class AddToCartSerializer(serializers.Serializer):

    quantity = serializers.IntegerField(min_value=1, required=False, default=1)