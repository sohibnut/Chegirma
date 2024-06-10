import uuid
from rest_framework import generics
from .models import Taqoslash
from .serializers import TaqoslashSerializer
from django.shortcuts import render
from django.db.models import Q
from .models import Comment, Product
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CommentSerializer
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from ..base.enum import CommentType
from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import WishListAddSerializer, ProductCategorySerializer
from django.shortcuts import get_object_or_404
from apps.accounts.models import UserModel
from .models import WishlistItem
from rest_framework.response import Response
from apps.base.utility import CustomPagination
from .models import WishlistItem, Product
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import filters


class TaqoslashView(generics.ListAPIView):
    serializer_class = TaqoslashSerializer

    def get_queryset(self):
        product_uuid = self.request.GET.getlist("product_uuid")
        return Taqoslash.objects.filter(product__in=product_uuid)[
            :5
        ]  # Limit to 5 products


class ProductCategoryview(APIView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = ProductCategorySerializer

    def get(self, request, uuid):
        querset = Product.objects.filter(category=uuid)  # children is not pulli
        serializer_data = self.serializer_class(querset, many=True)
        return Response(serializer_data.data)


class ProductSellerView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ProductCategorySerializer

    def get(self, request, uuid):
        queryset = Product.objects.filter(seller=uuid)
        serializer_data = self.serializer_class(queryset, many=True)
        return Response(serializer_data.data)


class ProductListView(ListAPIView):
    serializer_class = ProductCategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Product.objects.all()

        category_uuid = self.request.query_params.get("category_uuid", None)
        color_uuid = self.request.query_params.getlist("color_uuid", None)
        print(color_uuid)
        max_price = self.request.query_params.get("max_price", None)
        min_price = self.request.query_params.get("min_price", None)
        size = self.request.query_params.getlist("size", None)

        if category_uuid:
            queryset = queryset.filter(category__uuid=category_uuid)
        if color_uuid:
            queryset = queryset.filter(color__uuid__in=color_uuid)
        if min_price:
            queryset = queryset.filter(discount_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(discount_price__lte=max_price)
        if size:
            queryset = queryset.filter(size__uuid__in=size)
        return queryset


class SearchFilterView(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductCategorySerializer
    filter_backends = [filters.SearchFilter]  ####
    search_fields = ["color__name"]


class ProductByColorListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductCategorySerializer

    def get_queryset(self):
        color_uuid = self.kwargs[
            "color_uuid"
        ]  # assuming the color UUID is passed in the URL
        return Product.objects.filter(color__uuid=color_uuid)


class ProductListPriceView(generics.ListAPIView):
    serializer_class = ProductCategorySerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Product.objects.all()
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")

        if min_price is not None:
            queryset = queryset.filter(discount_price__gte=min_price)

        if max_price is not None:
            queryset = queryset.filter(discount_price__lte=max_price)

        return queryset


class WishListAddApiView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = WishListAddSerializer

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(UserModel, username=request.user.username)
        request.data["user"] = user.uuid
        data = request.data
        product = data.get("product")
        serializer = self.serializer_class(data=data)
        # TODO: delete wishlist
        check_cloth = WishlistItem.objects.filter(product__uuid=product).first()
        if check_cloth:
            check_cloth.delete()
            response_data = {
                "status": True,
                "message": f"Wish Listdan o'chirildi bu mahsulot --->  {product}",
            }
            return Response(response_data)
        # TODO: create wishlist
        elif serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data = {
                "status": True,
                "message": f"Wish Listga qo'shildi --->  {product}",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)


class WishlistGetApiView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        try:
            products = WishlistItem.objects.filter(user__username=request.user.username)
            serializer = WishListAddSerializer(products, many=True)
            count = len(serializer.data)
            data = {
                "status": True,
                "data": serializer.data,
                "count": count,
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            data = {"status": False, "message": f"{e}"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class NewCommentView(APIView):
    def get(self, request):
        product_data = Product.objects.all().values_list()
        user_data = UserModel.objects.all().values_list()
        for i in product_data:
            if request.data["product_id"] == str(i[1]):
                for j in user_data:
                    if str(j[9]) == request.data["author_id"]:
                        data = Comment(
                            product=Product.objects.filter(
                                uuid=request.data["product_id"]
                            )[0],
                            author=UserModel.objects.filter(
                                uuid=request.data["author_id"]
                            )[0],
                            type="New",
                            text=request.data["text"],
                        )
                        data.type = "new"
                        data.save()
                        return Response({"status": True})
        return Response({"status": False})


class ReplyCommentView(APIView):
    def get(self, request):
        user_data = UserModel.objects.all().values_list()
        comment_data = Comment.objects.all().values_list()
        for i in comment_data:
            if str(i[1]) == request.data["comment_id"]:
                for j in user_data:
                    if request.data["author_id"] == str(j[9]):
                        data = Comment(
                            product=Product.objects.filter(uuid=str(i[4]))[0],
                            author=UserModel.objects.filter(
                                uuid=request.data["author_id"]
                            )[0],
                            type="reply",
                            text=request.data["text"],
                        )
                        data.type = "reply"
                        data.save()
                        return Response(
                            {
                                "status": True,
                            }
                        )
        return Response({"status": False})
