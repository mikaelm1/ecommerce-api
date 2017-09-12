from authentication.tests import BaseTests


class BillingsRoutesTests(BaseTests):
    def test_create_cc_already_exists(self):
        url = '/billings/add-card'
        user = self.register_user(1, email_verified=True, with_cart=True)
        self.create_card(user)
        self.auth_client(user)
        data = {
            'exp_month': 10,
            'exp_year': 2020,
            'card_number': 1234123412341234,
            'stripe_token': 'test_token',
            'cvc': 123
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.data.get('detail'),
                         'User has already registered a credit card.')

    def test_create_cc_invalid_data(self):
        url = '/billings/add-card'
        user = self.register_user(1, email_verified=True, with_cart=True)
        self.auth_client(user)
        res = self.client.post(url)
        self.assertEqual(res.status_code, 400)

    def test_create_cc_valid(self):
        url = '/billings/add-card'
        user = self.register_user(1, email_verified=True, with_cart=True)
        self.assertEqual(user.creditcard_set.count(), 0)
        self.auth_client(user)
        data = {
            'exp_month': 10,
            'exp_year': 2020,
            'card_number': 1234123412341234,
            'stripe_token': 'test_token',
            'cvc': 123
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(user.creditcard_set.count(), 1)
