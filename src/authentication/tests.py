from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework import status
from django.conf import settings
from django.db.models import Q
from .models import User


@override_settings(TESTING=True)
class AuthenticationRoutesTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(AuthenticationRoutesTests, cls).setUpClass()

    def register_user(self, seed):
        """
        Helper to create a user object.
        :param seed: int
        """
        username = 'user{}'.format(seed)
        email = '{}@example.com'.format(username)
        user = User(username=username, email=email)
        user.set_password('pass')
        user.save()
        return user

    def user_by_identifier(self, ident):
        return User.get_by_identifier(ident)

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
