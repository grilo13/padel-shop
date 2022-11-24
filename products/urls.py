from django.urls import path
from .views import GetShoes

urlpatterns = [
    path('shoes', GetShoes.as_view(), name='get_shoes'),
]
