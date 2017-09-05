from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer, ItemCreateSerializer


class ItemsView(APIView):
    """
    get:
    Returns all items available for sale.
    post:
    Create a new item.
    """
    def get(self, req):
        items = Item.objects.filter(on_sale=True)
        print(ItemSerializer(items, many=True))
        return Response({'items': ItemSerializer(items, many=True).data})

    def post(self, req):
        if req.user.is_staff is False:
            return Response({'error': 'Only admins allowed to create items.'},
                            status=401)
        data = req.data
        data['seller'] = req.user.id
        serializer = ItemCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(ItemCreateSerializer(serializer.instance).data,
                            status=201)
        return Response({'errors': serializer.errors}, status=400)
