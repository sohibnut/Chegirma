from django.shortcuts import render
from rest_framework.generics import CreateAPIView,UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializer import SignUpSerializer,PersonalDataSerializer,LoginSerializer,LogoutSerializers
from .models import UserModel
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
import datetime




class SignUpApiView(CreateAPIView):
    permission_classes = (AllowAny, )
    queryset = UserModel.objects.all()
    serializer_class = SignUpSerializer

class VerifyCodeApiView(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')
        self.check_code(user, code)
        
        data = {
            'status' : True,
            'step' : user.step,
            'access' : user.token()['access'],
            'refresh' : user.token()['refresh']
        }
        return Response(data)
        
    @staticmethod
    def check_code(user, code):
        verify_code = user.verify_code.filter(code_lifetime__gte=datetime.now(), code=code, is_confirmed=False)
        
        if not verify_code.exists():
            data = {
                'status' : False,
                'message' : "Code vaqti tugagan yoki Code yaroqsiz"
            }
            raise ValidationError(data)
        
        else:
            verify_code.update(is_confirmed=True)
            
        if user.step == 'sent_email':
            user.step = 'verify_code'
            user.save()
        return True
    


class PersonalDataUpdadeApiView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PersonalDataSerializer
    http_method_names = ['put', 'patch']
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        super(PersonalDataUpdadeApiView, self).update(request, *args, **kwargs)
        data = {
            'status' : True,
            'message' : 'Ruyxatdan muvafaqiyatli otdingiz',
            'auth_status' : self.request.user.step
        }
        return Response(data)
    
    
    
    def partial_update(self, request, *args, **kwargs):
        super(PersonalDataUpdadeApiView, self).partial_update(request, *args, **kwargs)
        data = {
            'status' : True,
            'message' : 'Ruyxatdan muvafaqiyatli otdingiz',
            'auth_status' : self.request.user.step
        }
        return Response(data)
    




class LoginApiView(TokenObtainPairView):
    serializer_class = LoginSerializer
    


class LogoutApiView(APIView):
    serializer_class = LogoutSerializers
    permission_classes = (IsAuthenticated, )
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            refresh_token = self.request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                "status" : True,
                "message" : "Siz tizimdan chiqdiz"
            }
            
            return Response(data, status=205)
        except Exception as e:
            data = {
                "status" : False,
                "message" : str(e)
            }
            return Response(data, status=400)

