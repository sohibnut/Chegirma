from rest_framework import serializers
from .models import Comment, Compare, Product, WishlistItem

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):

    seller_name = serializers.SerializerMethodField("get_seller_name")
    comments_count = serializers.SerializerMethodField("get_comments_count")

    class Meta:
        model = Product
        fields = "__all__"

    @staticmethod
    def get_seller_name(obj):
        return obj.seller.name

    @staticmethod
    def get_comments_count(obj):
        return obj.product_comments.count()
        

class CompareSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    class Meta:
        model = Compare
        fields = "__all__"  # Add more fields if needed

class WishListAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ["product", "user"]