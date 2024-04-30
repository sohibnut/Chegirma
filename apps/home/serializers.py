from rest_framework import serializers
from .models import WishlistItem


class WishListAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ["product", "user"]

