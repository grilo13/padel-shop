import json
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

# Serializers
from .serializers import ShoeSerializer, ShoeAvailabilitySerializer

# Models
from .models import Shoes, ShoeAvailability, Racket, RacketAvailability

# Numpy
import numpy as np


# Create your views here.
class Index(APIView):
    def get(self, request):
        rackets = Racket.objects.order_by("?")
        shoes = Shoes.objects.order_by("?")

        mixed_products = np.random.choice(np.concatenate([rackets, shoes]), rackets.count() + shoes.count(),
                                          replace=False)

        return render(request, 'index.html', context={'products': mixed_products})


class GetShoes(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        shoes = Shoes.objects.all()

        context = {'shoes': shoes, 'count': shoes.count()}
        return render(request, 'products.html', context)


class GetSpecificShoeInformation(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, shoe_identifier):
        try:
            shoe = Shoes.objects.get(id=shoe_identifier)
        except Shoes.DoesNotExist:
            context = {'error': 'Shoe does not exist...'}
            return render(request, 'product.html', context)

        shoe_availability = ShoeAvailability.objects.filter(shoe_id=shoe_identifier)

        return render(request, 'product.html', context={'shoe': shoe, 'availability': shoe_availability})


class GetAvailabilityShoe(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        shoe_id = request.GET['shoe_id']
        shoe_size = request.GET['shoe_size']
        print(shoe_id, shoe_size)

        if shoe_size is not None:
            shoe_availability = ShoeAvailability.objects.get(shoe=shoe_id, size=shoe_size)
            serializer = ShoeAvailabilitySerializer(shoe_availability)
        else:
            shoe_availability = ShoeAvailability.objects.get(shoe=shoe_id)
            serializer = ShoeAvailabilitySerializer(shoe_availability, many=True)

        return Response(serializer.data, status=HTTP_200_OK)


class GetRackets(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        rackets = Racket.objects.all()

        context = {'rackets': rackets, 'count': rackets.count()}
        return render(request, 'rackets.html', context=context)


class GetSpecificRacketInformation(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, racket_identifier):
        try:
            racket = Racket.objects.get(id=racket_identifier)
        except Racket.DoesNotExist:
            return render(request, 'racket.html', context={'error': 'Racket not found...'})

        racket_availability = RacketAvailability.objects.filter(racket=racket_identifier)

        return render(request, 'racket.html', context={'racket': racket, 'availability': racket_availability})
