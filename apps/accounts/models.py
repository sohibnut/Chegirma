from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from apps.base.enum import UserRol, Tariff, UserStep
from apps.base.models import BaseModel

# Create your models here.

class UserModel(BaseModel,AbstractUser):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=UserRol.choices())
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    inn = models.CharField(max_length=255, null=True, blank=True)
    step = models.CharField(max_length=20, choices=UserStep.choices())
    def __str__(self) -> str:
        return self.name



class ContactModel(BaseModel):

    seller = models.OneToOneField(UserModel,on_delete=models.CASCADE, related_name='user_contact')
    image = models.ImageField(upload_to='seller/avatars/', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'heic', 'heif'])
    ])
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    site = models.CharField(max_length=255, null=True, blank=True)
    tg_link = models.CharField(max_length=255, null=True, blank=True)
    disc = models.TextField(null=True, blank=True)
    banner = models.ImageField(upload_to='seller/banners/', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'heic', 'heif'])
    ])
    tarif = models.CharField(max_length=10, choices=Tariff.choices(), default='default')


    def __str__(self) -> str:
        return f"contact - {self.seller.name}"
