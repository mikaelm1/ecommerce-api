from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_jwt.settings import api_settings


class User(AbstractUser):
    email_verified = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=255, blank=True, null=True)

    def to_json(self):
        res = {
            'email': self.email,
            'username': self.username,
        }
        return res

    @classmethod
    def get_by_identifier(self, identifier):
        """
        Find User by either email or username.
        """
        return self.objects.filter(
                    models.Q(username=identifier) |
                    models.Q(email=identifier)
                ).first()

    def get_jwt_token(self):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self)
        token = jwt_encode_handler(payload)
        return token
