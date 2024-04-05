from django.contrib import admin
from django.utils.safestring import mark_safe

from shop.models import Category


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

