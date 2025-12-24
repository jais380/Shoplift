from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.


class Product(models.Model):

    CATEGORY_CHOICES = (
        ("CL", "Clothes"),
        ("AC", "Accessories"),
        ("FW", "Footwears"),
        ("GA", "Gadgets"),
        ("EX", "Extras"),
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    in_stock = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name
    

class Cart(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    created = models.DateTimeField(auto_now_add=True)

    # Adds constaints metadata to limit one pending cart per user
    class Meta:
        ordering = ["-created"]
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=Q(status='PENDING'),
                name='one_pending_cart_per_user'
            )
        ]
    
    # Calculation for the total price of the items in a cart
    @property
    def total_price(self):
        return sum(
            item.product.price * item.quantity
            for item in self.items.all()
        )
    
    # Number of items in a cart
    @property
    def items_count(self):
        return self.items.count()
    

    def __str__(self):
        return f"{self.user.username} - {self.status}"
    

class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    # Adds constaints metadata to limit one product per cart
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="one_product_per_cart"
            )
        ]

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
