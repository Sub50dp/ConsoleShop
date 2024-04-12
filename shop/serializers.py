from rest_framework import serializers


from shop.models import Category, Feature, Product


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False)
    count_products = serializers.ReadOnlyField()
    name = serializers.CharField(required=False)

    class Meta:
        model = Category
        fields = ['name', 'image', 'count_products']


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['name', 'value']


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False)
    category = serializers.StringRelatedField()
    features = FeatureSerializer(many=True)
    slug = serializers.ReadOnlyField()
    rating = serializers.ReadOnlyField(source='average_rating')

    class Meta:
        model = Product
        fields = ['name', 'slug', 'image', 'category', 'features', 'price', 'count', 'description',
                  'available', 'brand', 'conditions', 'year_released', 'rating']


class CreateProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Product
        fields = ['name', 'image', 'category', 'features', 'price', 'count', 'description',
                  'available', 'brand', 'conditions', 'year_released']


