from rest_framework.urls import path
from .views import ProductCategoryView, SellerView, ProductListView, ProductPriceView

urlpatterns = [
    path("category/<uuid:uuid>/", ProductCategoryView.as_view()),
    path("seller/<uuid:uuid>/", SellerView.as_view()),
    path('product/', ProductListView.as_view()),
    path('price/', ProductPriceView.as_view()),
]
