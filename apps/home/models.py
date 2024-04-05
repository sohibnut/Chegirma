from django.db import models
from apps.base.models import BaseModel
from mptt.models import MPTTModel, TreeForeignKey
from apps.accounts.models import UserModel
from apps.base.enum import CommentType, ProductStatus
from django.core.validators import FileExtensionValidator
# Create your models here.




class Category(MPTTModel, BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    def __str__(self):
        return self.name
    
class Size(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_size')
    def __str__(self):
        return self.name
    
class Color(BaseModel):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class Product(BaseModel):
    seller = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='seller_product', blank=True)
    name = models.CharField(max_length=255)
    disc = models.TextField()
    image = models.ImageField(upload_to='seller/products/', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'heic', 'heif'])
    ])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_product', blank=True)
    original_price = models.BigIntegerField()
    discount_price = models.BigIntegerField()
    dis_start = models.DateField()
    dis_end = models.DateField()
    link = models.URLField(null=True, blank=True)
    size = models.ManyToManyField(Size, related_name='size_products')
    color = models.ManyToManyField(Color, related_name='color_products')
    status = models.CharField(max_length=10, choices=ProductStatus.choices())

    @property
    def get_descount(self):
        return (1 - self.discount_price/self.original_price) * 100
    
    def __str__(self) -> str:
        return self.name

class WishlistItem(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user_wishlistitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_wishlistitems')

    def __str__(self) -> str:
        return f"{self.user.name} -> WishListItem -> {self.product.name}"

class Comment(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comments', blank=True)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user_comments', blank=True)
    type = models.CharField(max_length=10,choices=CommentType.choices())
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='comment_reply')

    def __str__(self) -> str:
        return f"{self.author.name} -> comment -> {self.product.name}"