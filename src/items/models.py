from django.db import models
from authentication.models import User
from carts.models import Cart
from billings.models import PurchaseReceipt


class ItemInventory(models.Model):
    amount = models.IntegerField(default=1)

    def __str__(self):
        return "ID {} has {} items".format(self.id, self.item_set.count())


class Item(models.Model):
    title = models.CharField(max_length=255, db_index=True,
                             blank=False, null=False)
    notes = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=15, decimal_places=2,
                                blank=False, null=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, default=None, related_name='items_bought',
                              blank=True, null=True)
    on_sale = models.BooleanField(default=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True,
                             null=True)
    inventory = models.ForeignKey(ItemInventory, blank=True, null=True)

    class Meta:
        db_table = 'items'

    def __str__(self):
        return "{} with id {}".format(self.title, self.id)

    def price_in_cents(self):
        """
        Returns the price of the item in cents.
        """
        return int(self.price * 100)

    def to_json(self):
        res = {
            'id': self.id,
            'images': [i.to_json() for i in self.itemimage_set.all()],
            'title': self.title,
            'notes': self.notes,
            'date_posted': self.date_posted,
            'price': self.price,
            'on_sale': self.on_sale,
            'seller': self.seller.id,
            'buyer': self.buyer.id if self.buyer else None,
            'cart': self.cart.id if self.cart else None,
            'inventory': self.inventory.id,
        }
        return res


class ItemImage(models.Model):
    location = models.CharField(max_length=255, blank=False, null=False)
    item = models.ForeignKey(Item, blank=False, null=False)

    class Meta:
        db_table = 'item_images'

    def __str__(self):
        return 'Image for item {}'.format(self.item.title)

    def to_json(self):
        return {'location': self.location, 'id': self.id}


class PurchasedItem(models.Model):
    TRANSIT_STATUS = (
        # value, label
        ('Preparing', 'Preparing'),
        ('InTransit', 'InTransit'),
        ('Delivered', 'Delivered'),
    )
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    purchase_receipt = models.ForeignKey(PurchaseReceipt,
                                         on_delete=models.CASCADE)
    transit_status = models.CharField(
        max_length=40, choices=TRANSIT_STATUS,
        blank=False, null=False, default=TRANSIT_STATUS[0][0]
    )
