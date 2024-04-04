from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from apps.base.enum import UserRol,Tariff
from apps.base.models import BaseModel

# Create your models here.

class UserModel(BaseModel,AbstractUser):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=UserRol.choices())
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    inn = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.name



class ContactModel(BaseModel):

    seller = models.OneToOneField(UserModel,on_delete=models.CASCADE, related_name='user_contact')
    image = models.ImageField(upload_to='seller/avatars/', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'heic', 'heif'])
    ])
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    site = models.CharField(max_length=255)
    tg_link = models.CharField(max_length=255)
    disc = models.TextField()
    banner = models.ImageField(upload_to='seller/banners/', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'heic', 'heif'])
    ])
    tarif = models.CharField(max_length=10, choices=Tariff.choices())


    def __str__(self) -> str:
        return f"contact - {self.seller.name}"
