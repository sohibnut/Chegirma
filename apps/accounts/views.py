from django.shortcuts import render
from rest_framework.generics import CreateAPIView,APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializer import SignUpSerializer
from .models import UserModel
from rest_framework.response import Response






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
            'auth_status' : user.auth_status,
            'access' : user.token()['access'],
            'refresh' : user.token()['refresh']
        }
        return Response(data)