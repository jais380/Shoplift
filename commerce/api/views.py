from django.shortcuts import get_object_or_404
from django.db import transaction, IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend


from commerce.api.serializers import ProductSerializer, CartSerializer, CartItemSerializer
from commerce.models import Product, Cart, CartItem
from commerce.api.permissions import IsAdminorReadonly, IsCart
from commerce.api.pagination import ProductPagination, ChartItemPagination


class PendingCartAV(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get or create pending cart
        cart, _ = Cart.objects.get_or_create(user=self.request.user, status='PENDING')

        return cart



class CartItemAV(generics.ListCreateAPIView):

    serializer_class = CartItemSerializer

    permission_classes = [IsAuthenticated]
    pagination_class = ChartItemPagination

    def get_cart(self):
        # Ensure the cart belongs to the authenticated user
        return get_object_or_404(
            Cart,
            pk=self.kwargs['pk'],
            user=self.request.user
        )

    def get_queryset(self):
        cart = self.get_cart()
        # Return only items belonging to this cart
        return CartItem.objects.filter(cart=cart)

    
    # To ensure this method fails if any database operation fails
    @transaction.atomic
    def perform_create(self, serializer):
        cart = self.get_cart()

        # Raise error for any cart status other than pending
        if cart.status != 'PENDING':
            raise ValidationError("You can only add items to a pending cart.")

        product = serializer.validated_data["product"]
        quantity = serializer.validated_data.get("quantity", 1)

        try:
            # Get or create cart item
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={"quantity": quantity}
            )
        except IntegrityError:
            # Incase someone else created it simultaneously, safely fetch and update
            cart_item = CartItem.objects.select_for_update().get(cart=cart, product=product)
            created = False

        if not created:
            cart_item.quantity += quantity
            cart_item.save()




class CartItemDetailAV(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, IsCart]

    def get_cart(self):
        # Ensure the cart belongs to the authenticated user
        return get_object_or_404(
            Cart,
            pk=self.kwargs['pk'],
            user=self.request.user
        )

    def get_queryset(self):
        cart = self.get_cart()
        # Return only items belonging to this cart
        return CartItem.objects.filter(cart=cart)
    
    def perform_destroy(self, instance):
        # Raises error if the cart is not a pending cart to prevent deletion of cart items
        if instance.cart.status != 'PENDING':
            raise ValidationError("Cannot delete items from this cart")
        instance.delete()




class CartAV(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = CartSerializer

    def get_queryset(self):
        # Makes sure only one query each is sent to the database to fetch cart items and associated products in bulk
        return Cart.objects.filter(user=self.request.user).prefetch_related('items__product')

    
    def perform_create(self, serializer):

        # Raises error if pending cart already exists for the user.
        if Cart.objects.filter(user=self.request.user, status='PENDING').exists():
            raise ValidationError("Pending cart already exists")

        serializer.save(user=self.request.user)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']



class CartDetailAV(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated, IsCart]

    serializer_class = CartSerializer

    def get_queryset(self):
        # Makes sure only one query each is sent to the database to fetch cart items and associated products in bulk
        return Cart.objects.filter(user=self.request.user).prefetch_related('items__product')
        


class ProductCategoryAV(generics.ListAPIView):

    permission_classes = [AllowAny]
    pagination_class = ProductPagination

    serializer_class = ProductSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        # Filter products by category from the URL
        category = self.kwargs['categoryname']

        # Perform a case-insensitive match on the category code
        return Product.objects.filter(category__iexact=category)
    


class ProductAV(generics.ListCreateAPIView):

    permission_classes = [IsAdminorReadonly]
    pagination_class = ProductPagination

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ProductAVDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAdminorReadonly]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
