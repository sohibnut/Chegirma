from django.urls import include, path
from .views import WishListAddApiView, WishlistGetApiView


urlpatterns = [
    path('add-wish/', WishListAddApiView.as_view()),
    path('get-wish/', WishlistGetApiView.as_view()),
]
