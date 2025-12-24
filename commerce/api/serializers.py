from rest_framework import serializers
from commerce.models import Cart, Product, CartItem


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
    total_price = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    items_count = serializers.ReadOnlyField

    class Meta:

        model = Cart 
        fields = ['id', 'user', 'items', 'total_price', 'status', 'items_count', 'created']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:

        model = Product
        fields = '__all__'
    

    