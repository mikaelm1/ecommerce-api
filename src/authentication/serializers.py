from rest_framework import serializers
from .models import User


def validate_email(value):
    print('validating email')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username')
        # validators = [validate_email]

    def validate(self, data):
        return data
