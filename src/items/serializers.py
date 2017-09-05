from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('title', 'notes', 'price', 'seller', 'on_sale')

    def validate(self, data):
        return data
