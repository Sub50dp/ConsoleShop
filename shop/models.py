from django.db import models
from slugify import slugify


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, max_length=255)
    image = models.ImageField(upload_to='category/%Y-%m-%d/', blank=True, null=True)
    count_products = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.name))
        super().save(*args, **kwargs)

