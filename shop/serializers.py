from rest_framework import serializers


from shop.models import Category, Feature


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False)
    count_products = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ['name', 'image', 'count_products']


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['name', 'value']


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False)
    category = CategorySerializer()
    features = FeatureSerializer(many=True)

    class Meta:
        model = Category
        fields = ['name', 'image', 'category', 'features', 'price', 'count', 'description',
                  'available', 'brand', 'conditions', 'year_released']