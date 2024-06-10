from rest_framework import serializers
from .models import UserModel, ContactModel
from apps.base.utils import check_email, send_email, check_username, check_user
from rest_framework.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.generics import get_object_or_404
from django.contrib.auth.models import update_last_login
import uuid
from apps.base.utility import sent_email


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            'uuid',
            'step',
            'email'
        )
        extra_kwargs = {
            'uuid' : {'read_only' : True},
            'step' : {'read_only' : True, 'required' : False} 
        }

    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        code = user.create_code()
        user.username = user.email
        user.save()
        send_email(user.email, code)
        return user
    
    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data.update(instance.token())
        return data
    
class PersonalDataSerializer(serializers.Serializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, data):
        password = data.get('password', None)
        confirm_password = data.get('confirm_password')
        if password:
            validate_password(password)
            validate_password(confirm_password)
        
        if password != confirm_password:
            data = {
                'status' : False,
                'message' : 'Parollar mos emas'
            }
            raise ValidationError(data)
 
        return data
    
    def validate_username(self, username):
        if not check_username(username):
            data = {
                'status' : False,
                'message' : 'Username yaroqsiz'
            }
            raise ValidationError(data)
        if UserModel.objects.filter(username=username).exists():
            data = {
                'status' : False,
                'message' : 'Username mavjud'
            }
            raise ValidationError(data)
        
        return username
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
        if instance.step == 'verify_code':
            instance.step = 'complate'
        instance.token()
        instance.save()
        return instance
        
class LoginSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs) -> None:
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields['username'] = serializers.CharField(required = False, read_only=True)
        self.fields['user_input'] = serializers.CharField(required = True)
    
    def auth_validate(self, data):
        user_input = data.get('user_input')
        password = data.get('password')
        
        if check_user(user_input) == 'email':
         
            username = self.auth_user(user_input)
            
        else:
            data = {
                'status' : False,
                'message' : 'Siz Kiritgan malumotlarga mos foydalanuvchi topilmadi iltimos qaytadan tekshirib kiriting!'
            }
            raise ValidationError(data)
        
        
        
        user_kwargs = {
            self.username_field : username,
            "password" : password
        }
        
        user1 = UserModel.objects.get(username = username)
        if user1.step != "complate":
            data = {
            'status' : False,
                'message' : 'Siz hali Toliq ruyxatdan otmagansiz!'
            }
            raise ValidationError(data) 
        
        user = authenticate(**user_kwargs)
        if user is not None:
            self.user = user
        else:
            data = {
            'status' : False,
                'message' : 'User yoki parol xato'
            }
            raise ValidationError(data) 
        
    def auth_user(self, email):
        user = UserModel.objects.get(email = email)
        if not user:
            data = {
            'status' : False,
                'message' : 'Siz Kiritgan malumotlarga mos user topilmadi iltimos qaytadan tekshirib kiriting!'
            }
            raise ValidationError(data) 
        return user.username
    
    
    
    
    def validate(self, data):
        self.auth_validate(data)
        
        data = self.user.token()
        data['full_name'] = self.user.name
        
        return data
    
class LogoutSerializers(serializers.Serializer):
    refresh = serializers.CharField()

class SellerSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            'uuid',
            'step',
            'email',
            'inn'
        )
        extra_kwargs = {
            'step' : {'read_only' : True, 'required' : False}
        }

    def create(self, validated_data):
        inn = validated_data['inn']
        email = validated_data['email']
        if UserModel.objects.filter(inn=inn).exists():
            data = {
                'status' : False,
                'msg' : 'inn already exists'
            }
            raise ValidationError(data)
        if UserModel.objects.filter(email=email).exists():
            data = {
                'status' : False,
                'msg' : 'email already exists'
            }
            raise ValidationError(data)
        user = UserModel.objects.create(
            name = validated_data['inn'],
            username = validated_data['inn'],
            role='seller',
            email = validated_data['email'],
            inn = validated_data['inn'],
            step='sent_email'
        )
        code = user.create_code()
        sent_email(email=user.email, subject='chegirma tasdiqlash kodi',code=code)
        user.set_password(str(uuid.uuid4().__str__().split("-")[1]))
        user.save()
        return user
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(instance.token())
        return data    
    
class SellerDataSerializer(serializers.Serializer):
    name = serializers.CharField(write_only = True, required = True)
    password = serializers.CharField(write_only = True, required = True)
    confirm_password = serializers.CharField(write_only = True, required = True)

    def validate(self, data):
        password = data.get('password', None)
        confirm_password = data.get('confirm_password')
        if password:
            validate_password(password)
            validate_password(confirm_password)

        if password != confirm_password:
            edata = {
                'status' : False,
                'message' : 'passwords are not equal',
            }
            raise ValidationError(edata)
        

        return data
    

    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.set_password(validated_data.get('password'))
        if instance.step == 'verify_code':
            
            instance.step = 'complate'
        instance.save()
        return instance    
    
class UserContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactModel
        fields = '__all__'