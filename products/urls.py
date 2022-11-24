from django.urls import path
from .views import GetShoes, GetAvailabilityShoe

urlpatterns = [
    path('shoes', GetShoes.as_view(), name='get_shoes'),
    path('shoes/availability', GetAvailabilityShoe.as_view(), name='get_shoes_availability')
]
