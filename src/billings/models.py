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


class PurchaseReceiptManager(models.Manager):
    def find_by_id(self, id):
        return self.filter(id=id).first()


class PurchaseReceipt(models.Model):
    # Relationships
    # A relationship to PurchasedItems exists
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Credit card info
    brand = models.CharField(max_length=255)
    last_four = models.IntegerField()
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    # Purchase details
    stripe_id = models.CharField(max_length=255, db_index=True)
    currency = models.CharField(max_length=20)
    # The sum of all items purchased at the time
    amount = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    # Manager
    objects = PurchaseReceiptManager()

    def __str__(self):
        return "ID {} for {}".format(self.id, self.user.email)

    def get_items(self):
        return self.purchaseditem_set.all()
