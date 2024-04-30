from rest_framework import serializers
from .models import Taqoslash, Product, WishlistItem

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description']  # Adjust fields as needed

class TaqoslashSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Taqoslash
        fields = ['name', 'description']  # Add more fields if needed

class WishListAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ["product", "user"]