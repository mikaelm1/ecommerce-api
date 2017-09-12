from authentication.tests import BaseTests


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
