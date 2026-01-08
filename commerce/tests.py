from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status


from commerce.models import Product, Cart, CartItem

# Create your tests here.

class ProductAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="Jude", password="password")

        self.client.force_authenticate(user=self.user)

        self.product = Product.objects.create(name='Nike Jordans', description='Kicks on air', price='999.99', category='FW')

    def test_product_create(self):
        data = {
            "name":"Nike Jordans", 
            "description":"Kicks on air", 
            "price":999.99, 
            "category":"FW"
        }

        url = reverse('product-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)