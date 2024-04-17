# views.py
from rest_framework import generics
from rest_framework.response import Response
from .models import Taqoslash
from .serializers import TaqoslashSerializer

class CompareProductsView(generics.ListAPIView):
    serializer_class = TaqoslashSerializer

    def get_queryset(self):
        product_uuid = self.request.GET.getlist('product_uuid')
        return Taqoslash.objects.filter(product__in=product_uuid)[:5]  # Limit to 5 products


