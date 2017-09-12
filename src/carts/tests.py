from authentication.tests import BaseTests
from items.models import Item


class CartsRoutesTests(BaseTests):
    def test_cart_detail_not_auth(self):
        url = '/carts/cart'
        res = self.client.get(url)
        self.assertEqual(res.status_code, 401)

    def test_cart_detail_not_confirmed(self):
        user = self.register_user(1)
        url = '/carts/cart'
        self.auth_client(user)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.data.get('detail'),
                         'You have not verified your email address yet.')

    def test_cart_detail_valid(self):
        user = self.register_user(1, with_cart=True, email_verified=True)
        url = '/carts/cart'
        self.auth_client(user)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data.get('items')), 0)

    def test_add_to_cart_invalid_permissions(self):
        user = self.register_user(1)
        url = '/carts/add-item'
        res = self.client.put(url)
        self.assertEqual(res.status_code, 401)
        self.auth_client(user)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.data.get('detail'),
                         'You have not verified your email address yet.')

    def test_add_to_cart_invalid_inventory(self):
        user = self.register_user(1, with_cart=True, email_verified=True)
        url = '/carts/add-item'
        data = {'inventory_id': 100}
        self.auth_client(user)
        res = self.client.put(url, data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data.get('error'), 'Item not found.')

    def test_add_to_cart_empty_inventory(self):
        user = self.register_user(1, with_cart=True, email_verified=True)
        url = '/carts/add-item'
        inv = self.create_inventory()
        data = {'inventory_id': inv.id}
        self.auth_client(user)
        res = self.client.put(url, data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data.get('error'), 'Item is out of stock.')

    def test_add_to_cart_valid(self):
        user = self.register_user(1, with_cart=True, email_verified=True)
        url = '/carts/add-item'
        inv = self.create_inventory()
        item = self.create_item(1, user)
        self.add_item_to_inventory(inv, item)
        items_for_sale = inv.item_set.filter(on_sale=True)
        self.assertEqual(items_for_sale.count(), 1)
        data = {'inventory_id': inv.id}
        self.auth_client(user)
        res = self.client.put(url, data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(items_for_sale.count(), 0)

    def test_clear_cart_valid(self):
        url = '/carts/edit'
        user = self.register_user(1, with_cart=True, email_verified=True)
        self.auth_client(user)
        self.add_items_to_cart(user, num_items=2)
        self.assertEqual(user.cart.item_set.count(), 2)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(user.cart.item_set.count(), 0)

    def test_edit_cart_valid(self):
        url = '/carts/edit'
        user = self.register_user(1, with_cart=True, email_verified=True)
        self.auth_client(user)
        self.add_items_to_cart(user, num_items=2)
        self.assertEqual(user.cart.item_set.count(), 2)
        item_to_remove = user.cart.item_set.first()
        data = {'items': [item_to_remove.id]}
        res = self.client.put(url, data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(user.cart.item_set.count(), 1)
        updated_item = Item.objects.filter(id=item_to_remove.id).first()
        self.assertTrue(updated_item.on_sale)
        self.assertIsNone(updated_item.cart)
