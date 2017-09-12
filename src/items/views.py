from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Item, ItemInventory
from .serializers import (
    ItemSerializer, ItemCreateSerializer, ItemUpdateSerializer
)


class ItemsView(APIView):
    """
    get:
    Returns all items available for sale.
    post:
    Create a new item. Add it to inventory.
    """
    def get(self, req):
        items = Item.objects.filter(on_sale=True)
        # print(ItemSerializer(items, many=True))
        return Response({'items': ItemSerializer(items, many=True).data})

    def post(self, req):
        if req.user.is_staff is False:
            return Response({'error': 'Only admins allowed to create items.'},
                            status=401)
        data = req.data
        data['seller'] = req.user.id
        try:
            inv_id = int(data.get('inventory_id'))
        except:
            inv_id = None
        inv = ItemInventory.objects.filter(id=inv_id).first()
        if inv is None:
            # print('Inv is None')
            inv = ItemInventory.objects.create(amount=1)
        serializer = ItemCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            inv.item_set.add(serializer.instance)
            inv.amount = inv.item_set.count()
            inv.save()
            return Response(ItemSerializer(serializer.instance).data,
                            status=201)
        return Response({'errors': serializer.errors}, status=400)


class ItemDetailView(APIView):
    """
    get:
    Returns an item details
    put:
    Update an item
    """
    def get(self, req, id):
        item = Item.objects.filter(id=id).first()
        if item is None:
            return Response({'error': 'Item not found.'}, status=404)
        return Response(ItemSerializer(item).data)

    def put(self, req, id):
        if req.user.is_staff is False:
            return Response({'error': 'Only admins allowed to edit items.'},
                            status=401)
        item = Item.objects.filter(id=id).first()
        if item is None:
            return Response({'error': 'Item not found.'}, status=404)
        data = req.data
        serializer = ItemUpdateSerializer(item, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(ItemSerializer(item).data)
        return Response({'errors': serializer.errors}, status=400)
