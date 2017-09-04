from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email_verified = models.BooleanField(default=False)

    def to_json(self):
        res = {
            'email': self.email,
            'username': self.username,
        }
        return res
