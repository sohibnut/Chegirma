from django.shortcuts import render
from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import WishListAddSerializer, ProductCategorySerialize
from django.shortcuts import get_object_or_404
from apps.accounts.models import UserModel
from .models import WishlistItem, Product
from rest_framework.response import Response
from apps.base.utility import CustomPagination
# Create your views here.
from rest_framework.generics import ListAPIView, RetrieveAPIView
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




class WishListAddApiView(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = WishListAddSerializer 

    def post(self, request, *args, **kwargs):
        # user = get_object_or_404(UserModel, username=request.user)
        # request.data["user"] = user.uuid
        data = request.data
        product = data.get("product")
        serializer = self.serializer_class(data=data)
        ### delete wishlist
        check_cloth = WishlistItem.objects.filter(product=product).first()
        if check_cloth:
            check_cloth.delete()
            response_data = {"status": True, "message": f"Wish Listga o'chirildi {product}"}
            return Response(response_data)
        ### create wishlist
        elif serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data = {"status": True, "message": f"Wish Listga qo'shildi {product}"}
            return Response(response_data, status=status.HTTP_201_CREATED)
        


class WishlistGetApiView(APIView):
    permission_classes = [AllowAny, ]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        try:
            products = WishlistItem.objects.all().order_by("product")
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(products, request)
            
            # Get the requested page size from the query parameters
            page_size = request.query_params.get('page_size')

            # Set the page size in the paginator
            if page_size:
                paginator.page_size = page_size

            result_page = paginator.paginate_queryset(products, request)
            serializer = WishListAddSerializer(result_page, many=True)

            # Get the next and previous page URLs
            next_page = paginator.get_next_link()
            previous_page = paginator.get_previous_link()

            count = len(serializer.data)
            data = {
                "status": True,
                'next': next_page,
                'previous': previous_page,
                "data": serializer.data, 
                "count": count
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            data = {"status": False, "message": f"{e}"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


