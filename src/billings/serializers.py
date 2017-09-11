from rest_framework import serializers
from .models import CreditCard, PurchaseReceipt


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = '__all__'


class CreateCreditCardSerializer(serializers.Serializer):
    exp_month = serializers.IntegerField()
    exp_year = serializers.IntegerField()
    card_number = serializers.CharField()
    stripe_token = serializers.CharField()
    cvc = serializers.IntegerField()


class PurchaseReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseReceipt
        fields = '__all__'
