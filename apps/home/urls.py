from django.urls import path
from .views import TaqoslashView
from rest_framework.urls import path
from django.urls import re_path
from .views import( ProductCategoryview, ProductSellerView, SearchFilterView,
                    WishListAddApiView, WishlistGetApiView, ProductListView
                    ProductByColorListView, ProductListPriceView)

urlpatterns = [
    path("category/<uuid:uuid>/", ProductCategoryview.as_view(), name='categoryfilter'),
    path('product/', ProductListView.as_view()),
    path("seller/<uuid:uuid>/", ProductSellerView.as_view(), name='sellerfilter'),
    path("search/", SearchFilterView.as_view()), 
    re_path(r'^products/color/(?P<color_uuid>[a-f0-9-]+)/$', ProductByColorListView.as_view(), name='product-by-color'),
    path('products_price/', ProductListPriceView.as_view(), name='product-list'),
    path('add-wish/', WishListAddApiView.as_view()),
    path('get-wish/', WishlistGetApiView.as_view()),
    path('taqoslash/', TaqoslashView.as_view(), name='compare-products'),
]