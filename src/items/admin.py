from django.contrib import admin
from .models import Item, ItemInventory, PurchasedItem

admin.site.register(Item)
admin.site.register(ItemInventory)
admin.site.register(PurchasedItem)
