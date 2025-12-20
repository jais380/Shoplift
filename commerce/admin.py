from django.contrib import admin
from .models import Cart, CartItem, Product
# Register your models here.

admin.site.register(Cart)
admin.site.register(Product)
admin.site.register(CartItem)