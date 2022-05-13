from django.test import Client, TestCase
from requests import request
from authentication.models import CustomUser
from authentication.views import RegisterPage


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.mock_user = CustomUser.objects.create(
            email='mock@gmail.com',
            display_name='mock',
            password='testPassword!'
        )
    
    def test_registration(self):
        request = self.client.post('/register/', data={
            'email': 'test@gmail.com',
            'display_name': 'test',
            'password1': 'testPassword!',
            'password2': 'testPassword!'
        })

        test_user = CustomUser.objects.get(email='test@gmail.com')

        self.assertEquals(request.status_code, 302)
        self.assertEquals(test_user.email, 'test@gmail.com')
        self.assertEquals(CustomUser.objects.count(), 2)

    def test_login(self):
        request = self.client.post('/login/', data={
            'email': 'mock@gmail.com',
            'password': 'testPassword!'
        })

        self.assertEquals(request.status_code, 200)
