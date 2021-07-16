from rest_framework import permissions


# Create your permissions

class IsCustomerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.customer == request.user:
            return True
        return False


class IsCustomerOrReadOnlyForOrderItems(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.order.customer == request.user:
            return True
        return False