from rest_framework import serializers


from shop.models import Category


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False)
    count_products = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ['name', 'image', 'count_products']