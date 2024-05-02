from rest_framework import serializers
from .models import Comment, Product
from ..accounts.models import UserModel

class PrductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['uuid']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['uuid']

class CommentSerializer(serializers.ModelSerializer):
    product = PrductSerializer
    author = UserSerializer
    class Meta:
        model = Comment
        fields = ['product', 'author', 'text']

