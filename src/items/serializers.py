from rest_framework import serializers
from .models import Item, PurchasedItem


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('title', 'notes', 'price', 'seller', 'on_sale', 'inventory')
        # depth = 2

    def validate(self, data):
        return data


class ItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('title', 'notes', 'price', 'on_sale')

    def validate(self, data):
        return data


class PurchasedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedItem
        fields = '__all__'
