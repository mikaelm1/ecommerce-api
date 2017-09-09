from django.db import models
from authentication.models import User


class CreditCard(models.Model):
    name = models.CharField(max_length=255)
    last_four = models.IntegerField()
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=255)

    def __str__(self):
        return "{} for user {}".format(self.name, self.user)
