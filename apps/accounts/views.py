from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import UserModel
from datetime import datetime
from .signup_serializers import SellerSignUpSerializer, SellerDataSerializer, UserContactSerializer
# Create your views here.
class SellerSignUpApiView(CreateAPIView):
    permission_classes = (AllowAny, )
    model = UserModel 
    serializer_class = SellerSignUpSerializer

class VerifyCodeApiView(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')
        if self.check_code(user, code):
            data = {
                'status' : True,
                'message' : 'code verificated successfully',
                'auth_status' : user.step,
                'access' : user.token()['access'],
                'refresh' : user.token()['refresh']
            }
            return Response(data)
        else:
            data = {
                'status' : False,
                'message' : 'Invalid Code or time out'
            }
            raise ValidationError(data)
    
    @staticmethod
    def check_code(user, code):
        verify_code = user.verify_code.filter(code_lifetime__gte = datetime.now(), code = code, is_confirmed=False)
        if verify_code.exists() and user.step == 'sent_email':
            verify_code.update(is_confirmed = True)
            user.step = 'verify_code'
            user.save()
            return True
        else:
            return False
        
class SellerDataUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = SellerDataSerializer
    http_method_names = ['put', 'patch']

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        data = {
            'seller' : request.user.uuid,
            'tg_link' : request.data.get('tg_link'),
            'phone' : request.data.get('phone'),
            'banner' : request.data.get('banner'),
            'disc' : request.data.get('disc'),
            'site' : request.data.get('site'),
            'email' : request.data.get('email'),
            'image' : request.data.get('image'),
            'tarif' : 'default'
        }
        contact = UserContactSerializer(data=data)
        if contact.is_valid(raise_exception=True):
            contact.save()
            data = {
                "status" : True,
                'message' : 'You signed up successfully',
                'step' : self.request.user.step,
                'data' : contact.data
            }

            return Response(data)
    
     