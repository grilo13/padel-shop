import json

from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

# Serializers
from .serializers import ShoeSerializer, ShoeAvailabilitySerializer

# Models
from .models import Shoes, ShoeAvailability


# Create your views here.
class GetShoes(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        shoes = Shoes.objects.all()
        print(shoes)

        serializer = ShoeSerializer(shoes, many=True)

        return Response(serializer.data, status=HTTP_200_OK)


class GetAvailabilityShoe(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
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
