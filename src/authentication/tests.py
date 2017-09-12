from rest_framework.test import APITestCase
from .models import User


class AuthenticationRoutesTests(APITestCase):
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
