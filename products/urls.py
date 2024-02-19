from django.urls import path
from .views import GetShoes, GetSpecificShoeInformation, GetRackets, GetSpecificRacketInformation, \
    Index, GetItems, GetItemsMeasures, CheckWishlist, GetOrderItems, AddItemToWishlist

urlpatterns = [
    path('index', Index.as_view(), name='index'),
    path('shoes', GetShoes.as_view(), name='get_shoes'),
    path('items/', GetItems.as_view(), name='get_items'),
    path('items/<int:item_identifier>', GetItemsMeasures.as_view(), name='get_items_measures'),
    path('shoes/identifier/<int:shoe_identifier>', GetSpecificShoeInformation.as_view(), name='get_shoe_by_id'),
    path('rackets', GetRackets.as_view(), name='get_rackets'),
    path('racket/<int:racket_identifier>/', GetSpecificRacketInformation.as_view(), name='get_racket_by_id'),

    path('user/wishlist', CheckWishlist.as_view(), name='check_wishlist'),
    path('user/add/wishlist/<int:product>', AddItemToWishlist.as_view(), name='add_to_wishlist'),

    path('user/cart/', GetOrderItems.as_view(), name='get_order_items')
]
