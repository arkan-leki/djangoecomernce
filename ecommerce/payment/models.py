from django.db import models
from django.contrib.auth.models import User

from store.models import Product


# Create your models here.
class ShippingAddress(models.Model):
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    # optional
    state = models.CharField(max_length=250, null=True, blank=True)
    zip_code = models.CharField(max_length=250, null=True, blank=True)

    # author
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class meta:
        verbose_name = "shipping address"
        verbose_name_plural = "shipping addresses"

    def __str__(self):
        return self.full_name

    def __unicode__(self):
        return self.full_name
    


class Order(models.Model):
    STATUSES = (
        ("pending", "Order placed"),
        ("processing", "Product packaging"),
        ("shipped", "Ready for shipment"),
        ("trucking", "On the way"),
        ("arrived", "Dropped in the delivery station"),
        ("delivered", "Delivered"),
        ("out of stock", "Out of stock"),
    )
    
    # order_id = models.CharField(max_length=250, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    # shipping_address = models.ForeignKey(
    #     ShippingAddress, on_delete=models.CASCADE, null=True, blank=True
    # )
    shipping_address = models.TextField(max_length=1000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    # order_total = models.DecimalField(max_digits=10, decimal_places=2)

    # author
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # choice field
    order_status = models.CharField(max_length=20, choices=STATUSES, default="pending")

    class meta:
        verbose_name = "order"
        verbose_name_plural = "orders"

    def __str__(self):
        return "Order - #" + str(self.id)

    def __unicode__(self):
        return str(self.order_id)


class OrderItem(models.Model):
    # Order Item
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    # Product
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Item Details
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # author
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class meta:
        verbose_name = "order item"
        verbose_name_plural = "order items"

    def __str__(self):
        return "Order Item - #" + str(self.id)

    def __unicode__(self):
        return str(self.order_id)