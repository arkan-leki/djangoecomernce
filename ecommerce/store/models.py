from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)

    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        # db_table = 'category'
        # managed = True
        # verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("list-category", kwargs={"category_slug": self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=250, db_index=True)
    brand = models.CharField(max_length=250, default='un-branded')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    
    image= models.ImageField(upload_to='images/', blank=True)

    slug = models.SlugField(max_length=255)

    class Meta:
        # db_table = 'product'
        # managed = True
        # verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("product-info", kwargs={"product_slug": self.slug})
    
