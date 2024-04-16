import uuid
from rest_framework.views import APIView
from .serializers import ProductCategorySerializer
from .models import Product
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView


class ProductCategoryView(APIView):
    serializer_class = ProductCategorySerializer
    permission_classes = [AllowAny]

    def get(self, request, uuid):
        queryset = Product.objects.filter(category=uuid)
        serializer_data = self.serializer_class(queryset, many=True)
        return Response(serializer_data.data)


class SellerView(APIView):
    serializer_class = ProductCategorySerializer
    permission_classes = [AllowAny]

    def get(self, request, uuid):
        queryset = Product.objects.filter(seller=uuid)
        serializer_data = self.serializer_class(queryset, many=True)
        return Response(serializer_data.data)


class ProductListView(ListAPIView):
    serializer_class = ProductCategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Product.objects.all()

        category_uuid = self.request.query_params.get('category_uuid', None)
        color_uuid = self.request.query_params.getlist('color_uuid', None)
        print(color_uuid)
        max_price = self.request.query_params.get('max_price', None)
        min_price = self.request.query_params.get('min_price', None)
        size = self.request.query_params.getlist('size', None)

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
