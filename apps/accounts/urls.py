from django.urls import path
from .views import SellerSignUpApiView, VerifyCodeApiView, SellerDataUpdateView


urlpatterns = [
    path('seller_signup/', SellerSignUpApiView.as_view(), name='seller_sign_up'),
    path('verify_code/', VerifyCodeApiView.as_view(), name='verify_code'),
    path('seller_data/', SellerDataUpdateView.as_view(), name='seller_data'),
]
