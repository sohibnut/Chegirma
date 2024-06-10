from rest_framework import serializers
from .models import Comment, Taqoslash, Product, WishlistItem

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['product', 'author', 'text']

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description']  # Adjust fields as needed

class TaqoslashSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    class Meta:
        model = Taqoslash
        fields = "__all__"  # Add more fields if needed

class WishListAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ["product", "user"]