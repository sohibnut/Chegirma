from django.urls import path
from rest_framework.urls import path
from django.urls import re_path
from .views import( ProductCategoryview, ProductSellerView, SearchFilterView,
                    WishListAddApiView, WishlistGetApiView, ProductListView,
                    ProductByColorListView, ProductListPriceView, NewCommentView, 
                     ProductView, ComparingView, ReplyCommentView)

urlpatterns = [
    path("category/<uuid:uuid>/", ProductCategoryview.as_view(), name='categoryfilter'), #done
    path('products/', ProductListView.as_view()),        #done                                 
    path("seller/<uuid:uuid>/", ProductSellerView.as_view(), name='sellerfilter'),  #done
    path("search/", SearchFilterView.as_view()), 
    re_path(r'^products/color/(?P<color_uuid>[a-f0-9-]+)/$', ProductByColorListView.as_view(), name='product-by-color'),
    path('products_price/', ProductListPriceView.as_view(), name='product-list'),
    path('add-wish/', WishListAddApiView.as_view()),  #done
    path('get-wish/', WishlistGetApiView.as_view()),  #done
    path('compare/', ComparingView.as_view(), name='compare'), #done
    path('new_comment/', NewCommentView.as_view()), # done
    path('reply_comment/', ReplyCommentView.as_view()),
    path('product/', ProductView.as_view(), name='product') #done
]