from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from apps.base.enum import UserRol, Tariff, UserStep
from apps.base.models import BaseModel
from rest_framework_simplejwt.tokens import RefreshToken
import uuid
import random
from datetime import timedelta, datetime

# Create your models here.

class UserModel(BaseModel,AbstractUser):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=UserRol.choices())
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True,unique=True)
    inn = models.CharField(max_length=255, null=True, blank=True)
    step = models.CharField(max_length=20, choices=UserStep.choices(), default='sent_email')
    
    def __str__(self) -> str:
        return self.name

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access' : str(refresh.access_token),
            'refresh' : str(refresh)
        }
    
    def create_code(self):
        code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        UserConfirmation.objects.create(code = code, user = self)
        return code

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

CODE_LIFETIME = 3

class UserConfirmation(BaseModel):
    code = models.CharField(max_length = 6)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name = 'verify_code')
    code_lifetime = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.code}"
    
    def save(self, *args, **kwargs):
        self.code_lifetime = datetime.now() + timedelta(minutes=CODE_LIFETIME)
        super(UserConfirmation, self).save(*args, **kwargs)