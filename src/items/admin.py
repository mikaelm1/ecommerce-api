from django.contrib import admin
from .models import Item, ItemInventory, PurchasedItem, ItemImage

admin.site.register(Item)
admin.site.register(ItemInventory)
admin.site.register(PurchasedItem)
admin.site.register(ItemImage)