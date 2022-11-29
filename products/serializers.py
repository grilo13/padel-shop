from .models import Item, ItemMeasures, Wishlist
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ItemMeasuresSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemMeasures
        fields = '__all__'


class UserWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['item']
