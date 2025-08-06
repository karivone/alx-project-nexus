"""Custom permission classes"""

from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners to edit their objects"""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for owner
        return obj.user == request.user

class IsOwner(permissions.BasePermission):
    """Permission that only allows owners to access their objects"""
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsAdminOrOwner(permissions.BasePermission):
    """Permission for admin users or object owners"""
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user

class ReadOnlyOrAuthenticated(permissions.BasePermission):
    """Permission that allows read-only access to everyone and write access to authenticated users"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
