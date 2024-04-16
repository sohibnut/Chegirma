
from django.urls import path
from .views import (SignUpApiView,
                   VerifyCodeApiView,
                   PersonalDataUpdadeApiView,
                   LoginApiView,
                   LogoutApiView
                   )


urlpatterns = [
    path('signup/',SignUpApiView.as_view())

]
