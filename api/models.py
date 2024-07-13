from django.db import models

# Create your models here.

class ProductStatus(models.TextChoices):
    UPLOADED = "UPLOADED"
    REJECTED = "REJECTED"
    SUCCESS = "SUCCESS"
    CANCELLED = "CANCELLED"


class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    price = models.FloatField(default=0)
    status = models.CharField(max_length=50, choices=ProductStatus.choices, default=ProductStatus.UPLOADED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
