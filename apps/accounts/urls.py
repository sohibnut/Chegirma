from django.urls import path
from .views import (SignUpApiView, SellerSignUpApiView, SellerDataUpdateView,
                   VerifyCodeApiView, SellerDataChangeView, 
                   PersonalDataUpdadeApiView,
                   LoginApiView,
                   LogoutApiView, 
                   PasswordChangeView,


                   )

urlpatterns = [
    path('signup/',SignUpApiView.as_view()),
    path('seller_signup/', SellerSignUpApiView.as_view(), name='seller_sign_up'),
    path('verify_code/', VerifyCodeApiView.as_view(), name='verify_code'),
    path('seller_data/', SellerDataUpdateView.as_view(), name='seller_data'),
    path('personal_data/',PersonalDataUpdadeApiView.as_view()),
    path('login/',LoginApiView.as_view()),
    path('logout/',LogoutApiView.as_view()),
    path('password_change/',PasswordChangeView.as_view()),
    path('change_seller_data/', SellerDataChangeView.as_view()),
]