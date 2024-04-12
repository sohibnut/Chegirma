from rest_framework.urls import path
from .views import ProductCategoryview, ProductSellerView, SearchFilterView


urlpatterns = [
    path("category/<uuid:uuid>/", ProductCategoryview.as_view(), name='categoryfilter'),
    path("seller/<uuid:uuid>/", ProductSellerView.as_view(), name='sellerfilter'),
    path("search/", SearchFilterView.as_view())
    
]
