from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from order.models import OrderItem, Order
from shop.serializers import ProductSerializer
from utils.validators import validate_card_number, validate_card_expiry, validate_card_cvc


class OrderSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(max_length=50, region="UA", required=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'phone_number', 'full_name', 'status', 'shipping_address', 'comment', 'count_items',
                  'total_price', 'create_date', 'shipping_type']
        only_read = ['user', 'count_items', 'total_price', 'create_date']


class FirstStepOrderSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(max_length=50, region="UA", required=True)
    class Meta:
        model = Order
        fields = ['shipping_address', 'phone_number', 'full_name', 'comment']
        extra_kwargs = {
            'shipping_address': {'required': True},
            'phone_number': {'required': True},
            'full_name': {'required': True},
        }


class SecondStepOrderSerializer(serializers.ModelSerializer):
    shipping_type = serializers.ChoiceField(choices=Order.SHIPPING_TYPE_CHOICES, default="free")
    class Meta:
        model = Order
        fields = ['shipping_type']


class ThirdStepOrderSerializer(serializers.Serializer):
    card_holder = serializers.CharField(max_length=255, required=True)
    card_number = serializers.CharField(max_length=255, required=True, validators=[validate_card_number])
    card_expiry = serializers.CharField(max_length=255, required=True, validators=[validate_card_expiry])
    card_cvc = serializers.CharField(max_length=255, required=True, validators=[validate_card_cvc])


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'sum_total']

    def to_representation(self, instance):
        data = ProductSerializer(instance.product).data
        data['id'] = instance.id
        data['quantity'] = instance.quantity
        data['sum_total'] = instance.sum_total()
        return data
