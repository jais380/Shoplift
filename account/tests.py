from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.


class RegisterTests(APITestCase):

    def test_register(self):
        data = {
            "username": "jude",
            "email": "example159@example.com",
            "password": "password321#",
            "password2": "password321#"
        }

        url = reverse('register')

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, dict)


    def test_logout(self):
        data = {
            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2ODEzMzAyMCwiaWF0IjoxNzY4MDQ2NjIwLCJqdGkiOiI3ZTQ5N2FlYzYzOTU0ZDg4YmJiZGFlMDFiZmYwODg2ZSIsInVzZXJfaWQiOiIxIn0.009P__d4IcpQVBuX5WByC3L7_4Hg4oW8IIIsKL7VuFw"
        }

        url = reverse('logout')

        self.user = User.objects.create_user(username="jude", email="example159@example.com", password="password321#")
        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data['error'], 'Token does not belong to the user')