from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from slugify import slugify


from users.models import CustomUser


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


class Feature(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'value')


class Product(models.Model):

    YEAR_CHOICES = [(str(year), str(year)) for year in range(1950, timezone.now().year + 1)]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/%Y-%m-%d/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    available = models.BooleanField(default=False)
    brand = models.CharField(max_length=255, blank=True, null=True)
    conditions = models.CharField(choices=[('New', 'New'), ('Used', 'Used')], max_length=255, default='New')
    year_released = models.CharField(max_length=4, choices=YEAR_CHOICES)
    features = models.ManyToManyField(Feature, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.name))
        super().save(*args, **kwargs)

    @property
    def average_rating(self):
        ratings = ProductRating.objects.filter(product=self)
        if ratings.exists():
            average = sum(rating.rating for rating in ratings) / len(ratings)
            return round(average, 1)
        return 0


class ProductRating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=500, blank=True, null=True)
    rating = models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.rating}"


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def update_category_product_count(sender, instance, **kwargs):
    category = instance.category
    category.count_products = Product.objects.filter(category=category).count()
    category.save()