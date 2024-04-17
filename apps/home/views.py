from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializer import ProductCategorySerialize
from .models import Product
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import generics



class ProductCategoryview(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = ProductCategorySerialize
    
    def get(self , request, uuid):
         
        querset = Product.objects.filter(category = uuid )# children is not pulli
        serializer_data = self.serializer_class(querset, many = True)
        return Response(serializer_data.data)
    
class ProductSellerView(APIView):
    
    permission_classes = [AllowAny]
    serializer_class = ProductCategorySerialize
    
    def get(self, request, uuid):
        
        queryset = Product.objects.filter(seller = uuid)
        serializer_data = self.serializer_class(queryset, many = True)
        
        return Response(serializer_data.data)
    
    
class SearchFilterView(ListAPIView):
    
    permission_classes = (AllowAny, )
    queryset = Product.objects.all()
    serializer_class = ProductCategorySerialize
    filter_backends = [filters.SearchFilter]  ####
    search_fields = ['color__name']

class ProductByColorListView(generics.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ProductCategorySerialize

    def get_queryset(self):
        color_uuid = self.kwargs['color_uuid']  # assuming the color UUID is passed in the URL
        return Product.objects.filter(color__uuid = color_uuid)
    
# views.py

from django.db.models import Q


class ProductListPriceView(generics.ListAPIView):
    serializer_class = ProductCategorySerialize
    permission_classes = (AllowAny, )
    

    def get_queryset(self):
        queryset = Product.objects.all()
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price is not None:
            queryset = queryset.filter(discount_price__gte=min_price)
        
        if max_price is not None:
            queryset = queryset.filter(discount_price__lte=max_price)

        return queryset

