from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from .models import Cart
from items.models import Item, ItemInventory
from .serializers import CartSerializer

"""
Cart Flow:
Each item belongs to an Inventory. On adding an item to a cart, item's
on_sale property is set to False. Removing an item from a cart sets the item's
on_sale property to True. Checking out a cart deletes all items in the cart
and decrements each item's inventory by one for each item. An item's inventory's
amount property represents all the items it has, including ones that have on_sale
set to False.
"""


class CartDetailView(APIView):
    """
    Returns user's cart.
    """
    def get(self, req, uid):
        user = User.objects.filter(id=uid).first()
        if user is None:
            return Response({'error': 'User not found.'}, status=404)
        if req.user.is_staff is False and req.user.id != uid:
            return Response({'error': 'Can only view your own cart.'},
                            status=401)
        cart = user.cart
        items = cart.item_set.all()
        items = [i.id for i in items]
        # print(cart.to_json())
        return Response(cart.to_json())


class AddItemToCartView(APIView):
    """
    put:
    Add item to user's cart.
    """
    permission_classes = (IsAuthenticated,)

    def put(self, req):
        d = req.data
        inv = ItemInventory.objects.filter(id=d.get('inventory_id')).first()
        if inv is None:
            return Response({'error': 'Item not found.'}, status=404)
        items = inv.item_set.filter(on_sale=True)
        if items.count() <= 0:
            return Response({'error': 'Item is out of stock.'}, status=404)
        cart = req.user.cart
        item = items.first()
        item.cart = cart
        item.on_sale = False
        item.save()
        cart.item_set.add(item)
        # inv.amount -= 1
        # inv.save()
        # items.remove(item)
        return Response(cart.to_json())


class EditCartView(APIView):
    """
    put:
    Remove specific items from cart.
    delete:
    Remove all items from the cart.
    """
    permission_classes = (IsAuthenticated,)

    def put(self, req):
        cart = req.user.cart
        d = req.data
        items = d.get('items')
        cart_items = cart.item_set
        items_to_remove = []
        for i in cart_items.all():
            if i.id in items:
                # print('got id: {}'.format(i.id))
                # i.inventory.amount += 1
                # i.inventory.save()
                i.on_sale = True
                i.save()
                items_to_remove.append(i)
        for i in items_to_remove:
            cart_items.remove(i)
        return Response(cart.to_json())

    def delete(self, req):
        cart = req.user.cart
        cart_items = cart.item_set
        for i in cart_items.all():
            i.inventory.amount += 1
            i.inventory.save()
            i.on_sale = True
            i.save()
        cart_items.clear()
        return Response(cart.to_json())


class CheckoutView(APIView):
    """
    put:
    Purchase all items in user's cart.
    """
    permission_classes = (IsAuthenticated,)

    def put(self, req):
        # TODO: once payments implemented, charge user's credit card
        cart = req.user.cart
        items = cart.item_set
        for i in items.all():
            i.inventory.amount -= 1
            i.inventory.save()
        items.all().delete()
        # print(items.all())
        return Response(cart.to_json())
