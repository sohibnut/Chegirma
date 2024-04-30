from rest_framework import serializers
from .models import Category, Product


class ProductCategorySerialize(serializers.ModelSerializer):
    
    class Meta :
        model = Product
        fields = '__all__'