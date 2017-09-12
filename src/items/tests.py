from authentication.tests import BaseTests
from .models import Item, ItemInventory


class ItemsRoutesTests(BaseTests):
    def test_item_create_non_admin(self):
        url = '/items/'
        res = self.client.post(url)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.data.get('error'), 'Only admins allowed to create items.')

    def test_item_create_invalid_data(self):
        url = '/items/'
        user = self.register_user(1)
        user.is_staff = True
        user.save()
        data = {}
        self.auth_client(user)
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data.get('errors').get('title'),
                         ['This field is required.'])
    
    def test_item_create_valid(self):
        # Zero itmes in the db in the beginning
        items = Item.objects.all()
        self.assertEqual(items.count(), 0)
        # Zero inventory in db at first
        inv = ItemInventory.objects.all()
        self.assertEqual(inv.count(), 0)
        url = '/items/'
        user = self.register_user(1)
        user.is_staff = True
        user.save()
        data = {
            'title': 'Item1',
            'notes': 'Some notes about item.',
            'price': 20.25
        }
        self.auth_client(user)
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 201)
        # Should be 1 item and 1 inventory in db now
        items = Item.objects.all()
        self.assertEqual(items.count(), 1)
        inv = ItemInventory.objects.all()
        self.assertEqual(inv.count(), 1)
        # Item must be in newly created inventory
        self.assertTrue(items.first().inventory == inv.first())
