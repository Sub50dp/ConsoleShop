from shop.models import Product

import django_filters


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    min_year = django_filters.NumberFilter(field_name="year_released", lookup_expr='gte')
    max_year = django_filters.NumberFilter(field_name="year_released", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'min_year', 'max_year', 'brand', 'category__name', 'conditions', 'available']
