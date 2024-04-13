import uuid
from rest_framework.views import APIView
from .serializers import ProductCategorySerializer
from .models import Product
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView


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


class ProductListView(ListCreateAPIView):
    serializer_class = ProductCategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Product.objects.all()

        category_uuid = self.request.query_params.get('category_uuid', None)
        color_uuid = self.request.query_params.get('color_uuid', None)
        max_price = self.request.query_params.get('max_price')
        min_price = self.request.query_params.get('min_price')

        if category_uuid:
            queryset = queryset.filter(category__uuid=category_uuid)
        if color_uuid:
            queryset = queryset.filter(color__uuid=color_uuid)
        if min_price is not None:
            queryset = queryset.filter(discount_price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(discount_price__lte=max_price)
        return queryset
