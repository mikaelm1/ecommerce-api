from django.db import models
from authentication.models import User
from carts.models import Cart


class Item(models.Model):
    title = models.CharField(max_length=255, db_index=True,
                             blank=False, null=False)
    notes = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=15, decimal_places=2,
                                blank=False, null=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    on_sale = models.BooleanField(default=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'items'
