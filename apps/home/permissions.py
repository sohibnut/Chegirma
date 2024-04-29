from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from datetime import datetime, timezone
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from apps.base.enum import UserRol

class isAdmin(permissions.BasePermission):
    object_class = None
    role_method_name = UserRol.ADMIN
    
    def has_permission(self, request, view):
        if request.user.uuid is None:
            return False
        user = request.user
        if user.role == None:
            return False
        if self.role_method_name.value == user.role:
            try:
                token = OutstandingToken.objects.filter(user=user).order_by('-id')[0]
                block = BlacklistedToken.objects.filter(token=token)
                if not block:
                    return True
                else:
                    error = {
                        'detail' : f"Please login again"
                    }
                    raise ValidationError(error)
            except OutstandingToken.DoesNotExist:
                error = {
                    'detail' : f"DoesNotExist"
                }
                raise ValidationError(error)
        return True


class isSeller(permissions.BasePermission):
    object_class = None
    role_method_name = UserRol.SELLER
    
    def has_permission(self, request, view):
        if request.user.uuid is None:
            return False
        user = request.user
        if user.role == None:
            return False
        
        if self.role_method_name.value == user.role:
            try:
                token = OutstandingToken.objects.filter(user=user).order_by('-id')[0]
                block = BlacklistedToken.objects.filter(token=token)
                if not block:
                    return True
                else:
                    error = {
                        'detail': f"please login again"}
                    raise ValidationError(error)
            except OutstandingToken.DoesNotExist:
                error = {
                    'detail': f"DoesNotExist"}
                raise ValidationError(error)
        return True
class isClient(permissions.BasePermission):
    object_class = None
    role_method_name = UserRol.CLIENT
    
    def has_permission(self, request, view):
          
        user = request.user
        if getattr(user, 'role', None) != self.role_method_name:
            return False
        if self.role_method_name.value == user.role:
            try:
                token = OutstandingToken.objects.filter(user=user).order_by('-id')[0]
                block = BlacklistedToken.objects.filter(token=token)
                if not block:
                    return True
                else:
                    error = {
                        'detail': f"please login again"}
                    raise ValidationError(error)
            except OutstandingToken.DoesNotExist:
                error = {
                    'detail': f"DoesNotExist"}
                raise ValidationError(error)
        return True
    
class is_Authenticated(permissions.BasePermission):
    
    def has_permission(self, request, view):
          
        user = request.user
        if getattr(user, 'role', None) != self.role_method_name:
            return False
        if self.role_method_name.value == user.role:
            try:
                token = OutstandingToken.objects.filter(user=user).order_by('-id')[0]
                block = BlacklistedToken.objects.filter(token=token)
                if not block:
                    return True
                else:
                    error = {
                        'detail': f"please login again"}
                    raise ValidationError(error)
            except OutstandingToken.DoesNotExist:
                error = {
                    'detail': f"DoesNotExist"}
                raise ValidationError(error)
        return True