from django.contrib import admin
from .models import *
# Register your models here.

class UserModelAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid', 'password')
    list_display = ['username', 'name', 'email', 'phone', 'role']
    ordering = ['-created_at']

class ContactModelAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid', )
    list_display = ['seller', 'phone', 'email']
    ordering = ['-created_at']

admin.site.register(UserModel, UserModelAdmin)
admin.site.register(ContactModel, ContactModelAdmin)