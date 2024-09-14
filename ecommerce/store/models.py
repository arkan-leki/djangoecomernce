from django.db import models
from django.urls import reverse

class Collection(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/collections/', blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    products = models.ManyToManyField('Product', related_name='collections', blank=True)

    class Meta:
        verbose_name_plural = 'collections'

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.image:
            return self.image.url
        return ''
    
    def get_num_products(self):
        return self.products.count()

    def get_absolute_url(self):
        return reverse("collection-detail", kwargs={"collection_slug": self.slug})


class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    image = models.ImageField(upload_to='images/', blank=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def get_image_url(self):
        if self.image:
            return self.image.url
        return ''
    
    def get_absolute_url(self):
        return reverse("list-category", kwargs={"category_slug": self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=250, db_index=True)
    brand = models.CharField(max_length=250, default='un-branded')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.ImageField(upload_to='images/', blank=True)
    slug = models.SlugField(max_length=255)
    
    # Adding size and color as optional JSON fields
    size = models.JSONField(blank=True, null=True)  # Store size options in JSON format
    color = models.JSONField(blank=True, null=True)  # Store color options in JSON format

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title
    
    def get_image_url(self):
        if self.image:
            return self.image.url
        return ''
    
    def get_absolute_url(self):
        return reverse("product-info", kwargs={"product_slug": self.slug})
