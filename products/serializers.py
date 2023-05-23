from .models import Item, ItemMeasures, Wishlist
from rest_framework import serializers

LEAVE_EMPTY = 'Leave empty if no change needed'


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


class UserLoginSerializer(serializers.Serializer):
    """Your data serializer, define your fields here."""
    email = serializers.EmailField(help_text=LEAVE_EMPTY, style={'placeholder': 'Email'})
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text=LEAVE_EMPTY,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

