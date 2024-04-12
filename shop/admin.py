from django.contrib import admin
from django.utils.safestring import mark_safe

from shop.models import Category, Product, Feature, ProductRating


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'show_photo']
    prepopulated_fields = {'slug': ('name',)}
    fields = ['name', 'slug', 'image', 'show_photo']
    readonly_fields = ['show_photo']

    @admin.display(description='image')
    def show_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150">')
        else:
            return ''


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'get_average_rating', 'show_photo']
    prepopulated_fields = {'slug': ('name',)}
    fields = ['name', 'slug', 'category', 'image', 'show_photo', 'price', 'count', 'description', 'available', 'brand',
              'conditions', 'year_released', 'features', 'get_average_rating']
    readonly_fields = ['show_photo', 'get_average_rating']
    filter_horizontal = ('features',)

    @admin.display(description='Average Rating')
    def get_average_rating(self, obj):
        return obj.average_rating

    @admin.display(description='image')
    def show_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150">')
        else:
            return ''


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']
    fields = ['name', 'value']


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating']
    fields = ['product', 'user', 'rating']
    readonly_fields = ['product', 'user', 'rating']
