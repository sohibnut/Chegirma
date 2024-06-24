from django.urls import path
from .views import TaqoslashView
from rest_framework.urls import path
from django.urls import re_path
from .views import( ProductCategoryview, ProductSellerView, SearchFilterView,
                    WishListAddApiView, WishlistGetApiView, ProductListView,
                    ProductByColorListView, ProductListPriceView, NewCommentView, 
                    ReplyCommentView, ProductView)

urlpatterns = [
    path("category/<uuid:uuid>/", ProductCategoryview.as_view(), name='categoryfilter'), #done
    path('products/', ProductListView.as_view()),        #done                                 
    path("seller/<uuid:uuid>/", ProductSellerView.as_view(), name='sellerfilter'),  #done
    path("search/", SearchFilterView.as_view()), 
    re_path(r'^products/color/(?P<color_uuid>[a-f0-9-]+)/$', ProductByColorListView.as_view(), name='product-by-color'),
    path('products_price/', ProductListPriceView.as_view(), name='product-list'),
    path('add-wish/', WishListAddApiView.as_view()),  #done
    path('get-wish/', WishlistGetApiView.as_view()),    #done
    path('taqoslash/', TaqoslashView.as_view(), name='compare-products'),
    path('new_comment/', NewCommentView.as_view()),
    path('reply_comment/', ReplyCommentView.as_view()),
    path('product/', ProductView.as_view(), name='product')
]