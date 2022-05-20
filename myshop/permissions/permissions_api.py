from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

class IsOwnerOrReadOnlyComent(IsAuthenticated,permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class DefaultUserPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return not request.user.is_salesman

class SalesmanPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.is_salesman

class IsOwnerOrReadOnly(IsAuthenticated,permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            print(request.method)
            return True
        return obj.user == request.user



