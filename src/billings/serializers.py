from rest_framework import serializers
from .models import CreditCard


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = '__all__'



class CreateCreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ('name', 'last_four', 'expiration_date', 'user')
