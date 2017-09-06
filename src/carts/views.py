from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from .models import Cart
from items.models import Item


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
        return Response({'id': cart.id, 'user': cart.user.id, 'itmes': items})


class AddItemToCartView(APIView):
    """
    put:
    Add item to user's cart.
    """
    permission_classes = (IsAuthenticated,)

    def put(self, req):
        d = req.data
        item = Item.objects.filter(id=d.get('item_id')).first()
        if item is None:
            return Response({'error': 'Item not found.'}, status=404)
        cart = req.user.cart
        cart.item_set.add(item)
        item.inventory -= 1
        item.save()
        cart.save()
        print(cart.item_set.all())
        if item.inventory <= 0:
            item.delete()
        return Response({})
