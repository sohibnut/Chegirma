from rest_framework.urls import path
from .views import ProductCategoryView, SellerView

urlpatterns = [
    path("category/<uuid:uuid>/", ProductCategoryView.as_view()),
    path("seller/<uuid:uuid>/", SellerView.as_view()),
]
