from .models import Shoes, ShoeAvailability
from rest_framework import serializers


class ShoeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoes
        fields = '__all__'


class ShoeAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoeAvailability
        fields = '__all__'
