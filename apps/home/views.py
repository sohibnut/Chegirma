from rest_framework.views import APIView
from .serializers import ProductCategorySerializer
from .models import Product
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


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

