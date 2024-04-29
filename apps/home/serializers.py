from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.home.models import Product,ProductStatus

class SellerAddProduct(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'uuid',
            'name',
            'disc',
            'image',
            'category',
            'original_price',
            'discount_price',
            'dis_start',
            'dis_end',
            'link',
            'size',
            'color',
        )
        
    Product.status = ProductStatus.DRAFT
    
        