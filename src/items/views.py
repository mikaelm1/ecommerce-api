from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser
from .models import Item, ItemInventory, ItemImage
from .serializers import (
    ItemSerializer, ItemCreateSerializer, ItemUpdateSerializer,
    ItemImageSerializer
)


class ItemsView(APIView):
    """
    get:
    Returns all items available for sale.
    post:
    Create a new item. Add it to inventory.
    """
    def get(self, req):
        items = Item.objects.filter(on_sale=True).order_by('-date_posted')
        paginator = LimitOffsetPagination()
        paginated_items = paginator.paginate_queryset(items, req)
        # serialized = ItemSerializer(paginated_items, many=True).data
        serialized = [i.to_json() for i in paginated_items]
        return Response({'items': serialized})

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
            inv = ItemInventory.objects.create(amount=1)
        serializer = ItemCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            inv.item_set.add(serializer.instance)
            inv.amount = inv.item_set.count()
            inv.save()
            images = data.get('images', [])
            if len(images) > 0:
                for i in images:
                    img = ItemImage(location=i, item=serializer.instance)
                    img.save()
            return Response(serializer.instance.to_json(), status=201)
        return Response({'errors': serializer.errors}, status=400)


class ItemDetailView(APIView):
    """
    get:
    Returns an item details.
    put:
    Update an item.
    """
    def get(self, req, id):
        item = Item.objects.filter(id=id).first()
        if item is None:
            return Response({'error': 'Item not found.'}, status=404)
        return Response(item.to_json())

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


class ItemImageView(APIView):
    """
    put:
    Update an item's image.
    post:
    Create an image for an item.
    delete:
    Delete an item's image.
    """
    permission_classes = (IsAdminUser, )

    def put(self, req, id):
        image = ItemImage.objects.filter(id=id).first()
        if image is None:
            return Response({'detail': 'Image not found.'}, status=404)
        location = req.data.get('location')
        image.location = location
        image.save()
        return Response(ItemImageSerializer(image).data)

    def post(self, req, id):
        # the id is the id of the item
        item = Item.objects.filter(id=id).first()
        if item is None:
            return Response({'detail': 'Item not found.'}, status=404)
        if item.itemimage_set.count() >= 5:
            msg = 'Unable to add image to item. Item already has 5 images.'
            return Response({'detail': msg}, status=400)
        d = req.data
        d['item'] = item.id
        serializer = ItemImageSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(ItemImageSerializer(serializer.instance).data)
        return Response({'errors': serializer.errors}, status=400)

    def delete(self, req, id):
        image = ItemImage.objects.filter(id=id).first()
        if image is None:
            return Response({'detail': 'Image not found.'}, status=404)
        image.delete()
        return Response({}, status=204)
