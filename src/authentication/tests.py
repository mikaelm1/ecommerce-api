from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework import status
from django.conf import settings
from django.db.models import Q
from .models import User
from .tokens import account_activation_token
from items.models import Item, ItemInventory
from carts.models import Cart
from billings.models import CreditCard, PurchaseReceipt


@override_settings(TESTING=True)
class BaseTests(APITestCase):
    def register_user(self, seed, is_staff=False, with_cart=False,
                      email_verified=False):
        """
        Helper to create a user object.
        :param seed: int
        """
        username = 'user{}'.format(seed)
        email = '{}@example.com'.format(username)
        user = User(username=username, email=email)
        user.set_password('pass')
        if is_staff:
            user.is_staff = True
        if email_verified:
            user.email_verified = True
        user.save()
        if with_cart:
            cart = Cart(user=user)
            cart.save()
        return user

    def user_by_identifier(self, ident):
        return User.get_by_identifier(ident)

    def auth_client(self, user):
        """
        Sets the Authenication header on the test client.
        """
        token = user.get_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def create_item(self, seed, seller, price=12.00):
        """
        Creates an Item instance and returns it.
        """
        item = Item(
            title='Item{}'.format(seed),
            notes='Some notes.',
            seller=seller,
            price=price
        )
        item.save()
        return item

    def create_inventory(self, amount=1):
        """
        Creates an ItemInventory instance and returns it.
        """
        inv = ItemInventory(amount=amount)
        inv.save()
        return inv

    def add_item_to_inventory(self, inventory, item):
        """
        Adds an Item instance to an ItemInventory instance.
        """
        inventory.item_set.add(item)
        inventory.amount = inventory.item_set.count()
        inventory.save()

    def add_items_to_cart(self, user, num_items=1):
        """
        Adds N number of items to user's cart.
        """
        cart = user.cart
        inv = self.create_inventory(amount=0)
        for i in range(num_items):
            item = self.create_item(i, user)
            item.cart = cart
            item.on_sale = False
            item.save()
            self.add_item_to_inventory(inv, item)
            cart.item_set.add(item)

    def create_card(self, user):
        """
        Creates and returns a credit card for user.
        """
        card = CreditCard(
                name='Visa',
                last_four=1234,
                exp_month=11,
                exp_year=2020,
                user=user,
                stripe_id='stripe_id',
            )
        card.save()
        user.stripe_id = 'stripe_id'
        user.save()
        return card
    
    def create_receipt(self, user, seed):
        """
        Creates and returns a PurchaseReceipt instance for user.
        """
        receipt = PurchaseReceipt(
            user=user, brand='{}{}'.format(user, seed), last_four=1234,
            exp_month=10, exp_year=2020,
            currency='usd', amount=1080,
            stripe_id='test_stripe_id'
        )
        receipt.save()
        return receipt


class AuthenticationRoutesTests(BaseTests):
    @classmethod
    def setUpClass(cls):
        super(AuthenticationRoutesTests, cls).setUpClass()

    def test_register(self):
        user = self.register_user(1)
        url = '/auth/register/'
        data = {'username': user.username, 'email': user.email,
                'password': 'pwd'}
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 409)
        self.assertEqual(res.data.get('error'),
                         'An account with that email already exists.')
        data['email'] = 'user2@example.com'
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 409)
        self.assertEqual(res.data.get('error'),
                         'An account with that username already exists.')
        data['username'] = 'user2'
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 411)
        errMsg = ('Password must be at least {} '
                  'characters long'.format(settings.MIN_PASSWORD_LENGTH))
        self.assertEqual(res.data.get('error'), errMsg)
        data['password'] = 'pass'
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 200)
        user = self.user_by_identifier(data.get('email'))
        self.assertTrue(user is not None)
        self.assertTrue(user.cart is not None)

    def test_login(self):
        url = '/auth/login/'
        res = self.client.post(url)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.data.get('error'), 'Invalid login credentials.')
        user = self.register_user(1)
        data = {'identifier': user.username, 'password': 'pass'}
        # Can't login without verified email
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.data.get('error'), 'Your email is not verified.')
        user.email_verified = True
        user.save()
        # Test successful call
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.data.get('token'))

    def test_confirm_acct(self):
        url = '/auth/confirm-account/'
        res = self.client.get(url)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data.get('error'), 'uid must be an integer.')
        user = self.register_user(1)
        url += '?uid={}'.format(user.id * settings.EMAIL_CONFIRM_HASH_NUM)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data.get('error'), 'Invalid request data.')
        token = account_activation_token.make_token(user)
        url += '&token={}'.format(token)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_resend_confirm_email(self):
        url = '/auth/resend-email/'
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data.get('error'), 'Invalid user id.')
        user = self.register_user(1)
        url += '?uid={}'.format(user.id * settings.EMAIL_CONFIRM_HASH_NUM)
        res = self.client.get(url)
        self.assertTrue(res.status_code, 200)
        user.email_verified = True
        user.save()
        res = self.client.get(url)
        self.assertTrue(res.status_code, 400)
        self.assertTrue(res.data.get('error'), 'User email already verified.')


class UserModelTests(BaseTests):
    def test_user_email(self):
        user = User(email='user@example.com', username='user',
                    password='pass')
        self.assertFalse(user.email_verified)

    def test_get_by_identifier(self):
        user = User.get_by_identifier('wrong')
        self.assertIsNone(user)
        user = self.register_user(1)
        user = User.get_by_identifier(user.email)
        self.assertIsNotNone(user)
