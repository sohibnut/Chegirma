from django.contrib import admin
from .models import *
# Register your models here.

class AdminList(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['-created_at']    

admin.site.register(Category, AdminList)
admin.site.register(Color, AdminList)
admin.site.register(Size, AdminList)
admin.site.register(Product, AdminList)
admin.site.register(WishlistItem)
admin.site.register(Comment)