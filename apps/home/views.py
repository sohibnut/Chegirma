from django.shortcuts import render
from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import WishListAddSerializer
from django.shortcuts import get_object_or_404
from apps.accounts.models import UserModel
from .models import WishlistItem
from rest_framework.response import Response
from apps.base.utility import CustomPagination


class WishListAddApiView(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = WishListAddSerializer 

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(UserModel, username=request.user)
        request.data["user"] = user.uuid
        data = request.data
        product = data.get("product")
        serializer = self.serializer_class(data=data)
        #TODO: delete wishlist
        check_cloth = WishlistItem.objects.filter(product=product).first()
        if check_cloth:
            check_cloth.delete()
            response_data = {"status": True, "message": f"Wish Listga o'chirildi {product}"}
            return Response(response_data)
        #TODO: create wishlist
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

