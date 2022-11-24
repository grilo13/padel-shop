from .models import Shoes
from rest_framework import serializers


class ShoeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoes
        fields = '__all__'
