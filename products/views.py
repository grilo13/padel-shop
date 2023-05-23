import json
from django.shortcuts import render, redirect
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

# Serializers
from .serializers import ItemSerializer, ItemMeasuresSerializer, UserWishlistSerializer, UserLoginSerializer

# Models
from .models import Item, ItemMeasures, Category, Wishlist, Order
from django.contrib.auth.models import User, AnonymousUser

from django.contrib.auth import authenticate, login, password_validation, logout

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

        return render(request, 'layouts/base.html')


class GetItemsMeasures(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, item_identifier):
        item_measures = ItemMeasures.objects.filter(item=item_identifier)
        related_products = Item.objects.order_by('-date_added').filter(category=item_measures[0].item.category.id)

        user = request.user
        if user is not None:
            wishlist = Wishlist.objects.filter(user=user)
            if wishlist.filter(item=item_measures[0].item).count() > 0:
                is_wishlist = True
            else:
                is_wishlist = False

            user_order = Order.objects.filter(user=user).first()
            if user_order is None:
                number_of_items_cart = 0
            else:
                number_of_items_cart = user_order.get_number_of_items()
            return render(request, 'layouts/product.html',
                          context={'item_measures': item_measures, 'related_products': related_products,
                                   'wishlist_count': wishlist.count(), 'cart_items': number_of_items_cart,
                                   'is_wishlist': is_wishlist})
        else:
            return render(request, 'layouts/product.html',
                          context={'item_measures': item_measures, 'related_products': related_products})


class Index(APIView):
    def get(self, request):
        featured_products = Item.objects.order_by('-date_added').filter(is_featured=True)
        categories = Category.objects.all()

        user = request.user
        if type(user) is not AnonymousUser:
            wishlist = Wishlist.objects.filter(user=user).count()
            user_order = Order.objects.filter(user=user).first()
            if user_order is None:
                number_of_items_cart = 0
            else:
                number_of_items_cart = user_order.get_number_of_items()

            return render(request, 'layouts/base.html',
                          context={'categories': categories, 'featured_products': featured_products,
                                   'wishlist_count': wishlist, 'cart_items': number_of_items_cart})
        else:
            return render(request, 'layouts/base.html',
                          context={'categories': categories, 'featured_products': featured_products})


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
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        wishlist = Wishlist.objects.filter(user=user)

        return render(request, 'wishlist.html', context={'wishlist': wishlist, 'user': user})


class AddItemToWishlist(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, product):
        user = request.user
        wishlist = Wishlist.objects.filter(user=user, item=Item.objects.get(id=product))
        wishlist.delete()

        return redirect('get_items_measures', item_identifier=product)

    def post(self, request, product):
        user = request.user
        wishlist = Wishlist.objects.create(user=user, item=Item.objects.get(id=product))

        return redirect('get_items_measures', item_identifier=product)
