from django.db import models
from authentication.models import User


class CreditCard(models.Model):
    name = models.CharField(max_length=255)
    last_four = models.IntegerField()
    expiration_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
