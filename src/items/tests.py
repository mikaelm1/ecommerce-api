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

    def test_items_index_no_items(self):
        url = '/items/'
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data.get('items')), 0)

    def test_itmes_index_with_items(self):
        user = self.register_user(1)
        item = self.create_item(1, user)
        url = '/items/'
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data.get('items')), 1)
        self.assertEqual(res.data.get('items')[0].get('id'), item.id)

    def test_item_detail_invalid(self):
        url = '/items/item/100'
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)
    
    def test_item_detail_valid(self):
        user = self.register_user(1)
        item = self.create_item(1, user)
        url = '/items/item/{}'.format(item.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data.get('id'), item.id)

    def test_item_edit_nonadmin(self):
        user = self.register_user(1)
        item = self.create_item(1, user)
        url = '/items/item/{}'.format(item.id)
        res = self.client.put(url)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.data.get('error'),
                         'Only admins allowed to edit items.')

    def test_item_edit_invalid_id(self):
        url = '/items/item/100'
        user = self.register_user(1, is_staff=True)
        self.auth_client(user)
        res = self.client.put(url)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data.get('error'), 'Item not found.')

    def test_item_edit_valid(self):
        user = self.register_user(1, is_staff=True)
        item = self.create_item(1, user, price=10)
        url = '/items/item/{}'.format(item.id)
        data = {
            'title': 'New Title',
            'notes': 'New Notes',
            'price': 999.99
        }
        self.auth_client(user)
        res = self.client.put(url, data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data.get('title'), 'New Title')
        self.assertEqual(res.data.get('notes'), 'New Notes')
        self.assertEqual(res.data.get('price'), '999.99')
