from rest_framework import permissions
from commerce.models import Cart, CartItem


class IsAdminorReadonly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)
        

class IsCart(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Cart):
            return obj.user == request.user

        if isinstance(obj, CartItem):
            return obj.cart.user == request.user

        return False

        