from rest_framework import serializers


from shop.models import Category, Feature, Product, ProductRating


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


class EditProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False)
    features_add = serializers.ListField(child=serializers.IntegerField(), required=False)
    features_remove = serializers.ListField(child=serializers.IntegerField(), required=False)

    class Meta:
        model = Product
        fields = ['name', 'image', 'category', 'features_add', 'features_remove', 'price', 'count', 'description',
                  'available', 'brand', 'conditions', 'year_released']
        extra_kwargs = {
            'name': {'required': False},
            'category': {'required': False},
            'price': {'required': False},
            'year_released': {'required': False},
        }


class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ['rating', 'text']
        extra_kwargs = {
            'text': {'required': False},}


class EditRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ['rating', 'text']
        extra_kwargs = {
            'text': {'required': False},
            'rating': {'required': False},
        }
