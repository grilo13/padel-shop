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
from .models import Item, ItemMeasures, Category, Wishlist

# Numpy
import numpy as np


# Create your views here.

class GetItems(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
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
        rackets = Item.objects.order_by("?")

        return render(request, 'index.html', context={'products': rackets})


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

        shoe_availability = ItemMeasures.objects.filter(item=shoe_identifier)

        return render(request, 'shoe.html', context={'shoe': shoe, 'availability': shoe_availability})


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

        racket_availability = ItemMeasures.objects.filter(item=racket_identifier)

        return render(request, 'racket.html', context={'racket': racket, 'availability': racket_availability})


class CheckWishlist(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        user = request.user

        wishlist = Wishlist.objects.filter(user=user)

        return render(request, 'wishlist.html', context={'wishlist': wishlist, 'user': user})
