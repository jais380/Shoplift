from rest_framework import serializers
from commerce.models import Cart, Product, CartItem

from drf_spectacular.utils import extend_schema_field


class CartItemSerializer(serializers.ModelSerializer):

    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only = True)

    class Meta:

        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity']

    # To ensure that the quantity is not less than 1
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value


class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(many=True, read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)

    # Use SerializerMethodField for read-only computed fields
    total_price = serializers.SerializerMethodField()
    
    items_count = serializers.SerializerMethodField()


    class Meta:

        model = Cart 
        fields = ['id', 'user', 'items', 'total_price', 'status', 'items_count', 'created']

    # To ensure no other status except the ones in choices can be patched into the cart
    def validate_status(self, value):
        if value not in [status for status, _ in Cart.STATUS_CHOICES]:
            raise serializers.ValidationError("Invalid status")
        return value


    # Methods to compute the properties with schema hints
    @extend_schema_field(serializers.DecimalField(max_digits=10, decimal_places=2))
    def get_total_price(self, obj):
        return obj.total_price

    @extend_schema_field(serializers.IntegerField)
    def get_items_count(self, obj):
        return obj.items_count


class ProductSerializer(serializers.ModelSerializer):

    class Meta:

        model = Product
        fields = '__all__'

    # To ensure no other category except the ones in choices can be patched into the product
    def validate_category(self, value):
        if value not in [category for category, _ in Product.CATEGORY_CHOICES]:
            raise serializers.ValidationError("Invalid status")
        return value
    

    