from django.db import models
from authentication.models import User


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{}'s Cart".format(self.user.username)

    def to_json(self):
        res = {
            'id': self.id,
            'user_id': self.user.id,
            'items': [i.id for i in self.item_set.all()]
        }
        return res
