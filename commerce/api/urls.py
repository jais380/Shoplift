from django.urls import path

from commerce.api import views


urlpatterns = [
    path('products/', views.ProductAV.as_view(), name='product-list'),
    path('product/<int:pk>/', views.ProductAVDetail.as_view(), name='product-detail'),
    path('category/<str:categoryname>/products/', views.ProductCategoryAV.as_view(), name='product-category-list'),
    path('carts/', views.CartAV.as_view(), name='cart-list'),
    path('cart/<int:pk>/', views.CartDetailAV.as_view(), name='cart-detail'),
    path('cart/<int:pk>/items/', views.CartItemAV.as_view(), name='item-list'),
    path('cart/item/<int:pk>/', views.CartItemDetailAV.as_view(), name='item-list-detail'),
    path('cart/pending/', views.PendingCartAV.as_view(), name="pending-cart"),
]