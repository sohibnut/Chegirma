from rest_framework import serializers
from .models import UserModel, ContactModel
from django.contrib.auth.password_validation import validate_password
import uuid
from apps.base.utility import sent_email
from rest_framework.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

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