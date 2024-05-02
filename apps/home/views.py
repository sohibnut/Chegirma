from django.shortcuts import render
from ..accounts.models import UserModel
from .models import Comment, Product
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CommentSerializer
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from ..base.enum import CommentType
# Create your views here.

class NewCommentView(APIView):
    def get(self, request):
        product_data = Product.objects.all().values_list()
        user_data = UserModel.objects.all().values_list()
        for i in product_data:
            if request.data['product_id'] == str(i[1]):
                for j in user_data:  
                    if str(j[9]) == request.data['author_id']:
                        data = Comment(
                            product = Product.objects.filter(uuid=request.data['product_id'])[0],
                            author = UserModel.objects.filter(uuid=request.data['author_id'])[0],
                            type = "New",
                            text = request.data['text'],
                        )
                        data.type="new"
                        data.save()
                        return Response(
                            {
                                'status' : True
                            }
                        )    
        return Response(
            {
                'status' : False
            }
        )    
                             
     


class ReplyCommentView(APIView):
    def get(self, request):
        user_data = UserModel.objects.all().values_list()
        comment_data = Comment.objects.all().values_list()
        for i in comment_data:
            if str(i[1]) == request.data['comment_id']:
                for j in user_data:
                    if request.data['author_id'] == str(j[9]):
                        data = Comment(
                            product = Product.objects.filter(uuid=str(i[4]))[0],
                            author = UserModel.objects.filter(uuid=request.data['author_id'])[0],
                            type = 'reply',
                            text = request.data['text'],
                      
                        )
                        data.type = 'reply'
                        data.save()
                        return Response(
                            {
                                'status' : True,
                              
                            }
                        )    
        return Response(
            {
                'status' : False
            }
        )    
         