from django.db import models

# Create your models here.
class Nutriment(models.Model):
    name = models.CharField(max_length=255, unique=True)
    unit = models.CharField(max_length=2)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    url = models.URLField(max_length=255, unique=True)
    image_url = models.URLField(max_length=255, unique=True)
    nutri_score = models.CharField(max_length=1)
    nutriments = models.ManyToManyField('products.Nutriment', through='products.ProductNutriments')
    categories = models.ManyToManyField('products.Category', through='products.ProductCategories')

    def __str__(self):
        return self.name

class ProductNutriments(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    nutriment = models.ForeignKey('products.Nutriment', on_delete=models.CASCADE)
    quantity = models.FloatField()

class ProductCategories(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    category = models.ForeignKey('products.Category', on_delete=models.CASCADE)