from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Item


class ItemsView(APIView):
    """
    get:
    Returns all items available for sale.
    """
    def get(self, req):
        items = Item.objects.filter(on_sale=True).all()
        return Response({'items': items})
