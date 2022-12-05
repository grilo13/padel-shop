import json
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

# Serializers
from .serializers import ItemSerializer, ItemMeasuresSerializer, UserWishlistSerializer

# Models
from .models import Item, ItemMeasures, Category, Wishlist, Order

# Numpy
import numpy as np


# Create your views here.
class GetOrderItems(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        order = Order.objects.get(user=user)
        items = order.get_items_in_order()
        total_items = order.get_number_of_items()
        amount = order.get_amount()
        print(items)

        return render(request, 'order.html', context={'order': items, 'total_items': total_items, 'amount': amount})


class GetItems(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        order = Order.objects.get(id=1)
        print(order)
        print(order.get_amount())
        print(order.get_number_of_items())

        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)

        return Response(serializer.data, status=HTTP_200_OK)


class GetItemsMeasures(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, item_identifier):
        items = ItemMeasures.objects.filter(item=item_identifier)
        serializer = ItemMeasuresSerializer(items, many=True)

        return Response(serializer.data, status=HTTP_200_OK)


class Index(APIView):
    def get(self, request):
        recent_products = Item.objects.order_by('-date_added')

        featured_products = recent_products.filter(is_featured=True)

        return render(request, 'index.html', context={'recent_products': recent_products[:8],
                                                      'featured_products': featured_products[:4]})


class GetShoes(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        shoes_category = Category.objects.get(category='Shoes')
        shoes = Item.objects.filter(category=shoes_category)

        context = {'shoes': shoes, 'count': shoes.count()}
        return render(request, 'shoes.html', context)


class GetSpecificShoeInformation(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, shoe_identifier):
        try:
            shoe = Item.objects.get(id=shoe_identifier)
        except Item.DoesNotExist:
            context = {'error': 'Shoe does not exist...'}
            return render(request, 'shoe.html', context)

        reviews = shoe.get_reviews()
        average_rating = shoe.get_average_rating()
        shoe_availability = ItemMeasures.objects.filter(item=shoe_identifier)

        return render(request, 'shoe.html',
                      context={'shoe': shoe, 'availability': shoe_availability, 'average_rating': average_rating,
                               'reviews': reviews})


class GetRackets(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        racket_category = Category.objects.get(category='Racket')
        rackets = Item.objects.filter(category=racket_category)

        context = {'rackets': rackets, 'count': rackets.count()}
        return render(request, 'rackets.html', context=context)


class GetSpecificRacketInformation(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, racket_identifier):
        try:
            racket = Item.objects.get(id=racket_identifier)
        except Item.DoesNotExist:
            return render(request, 'racket.html', context={'error': 'Racket not found...'})

        reviews = racket.get_reviews()
        average_rating = racket.get_average_rating()
        racket_availability = ItemMeasures.objects.filter(item=racket_identifier)

        return render(request, 'racket.html',
                      context={'racket': racket, 'availability': racket_availability, 'average_rating': average_rating,
                               'reviews': reviews})


class CheckWishlist(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        user = request.user

        wishlist = Wishlist.objects.filter(user=user)

        return render(request, 'wishlist.html', context={'wishlist': wishlist, 'user': user})
