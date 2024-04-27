# urls.py
from django.urls import path
from .views import TaqoslashView

urlpatterns = [
    path('taqoslash/', TaqoslashView.as_view(), name='compare-products'),
]

