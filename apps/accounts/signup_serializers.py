from rest_framework import serializers
from .models import UserModel
import uuid
from apps.base.utility import sent_email

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
            'auth_status' : {'read_only' : True, 'required' : False}
        }

    def create(self, validated_data):
        user = UserModel.objects.create(
            name = validated_data['inn'],
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