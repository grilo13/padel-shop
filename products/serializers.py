from .models import Shoes, ShoeAvailability, Item, ItemMeasures
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ItemMeasuresSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemMeasures
        fields = '__all__'


class ShoeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoes
        fields = '__all__'


class ShoeAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoeAvailability
        fields = '__all__'
