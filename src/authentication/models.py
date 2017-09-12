from django.db import models
from django.contrib.auth.models import AbstractUser


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
