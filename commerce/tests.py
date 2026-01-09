from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status


from commerce.models import Product, Cart, CartItem

from decimal import Decimal

# Create your tests here.

class ProductAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="Jude", password="password")

        self.client.force_authenticate(user=self.user)

        self.product = Product.objects.create(name='Nike Jordans', description='Kicks on air', price= Decimal('999.99'), category='FW')

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

    def test_admin_can_create_product(self):
        self.user.is_staff = True
        self.user.save()
        data = {
            "name":"Nike Jordans", 
            "description":"Kicks on air", 
            "price":999.99, 
            "category":"FW"
        }

        url = reverse('product-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data['results'][0]['category'], 'FW')

    def test_product_individual(self):
        url = reverse('product-detail', args=(self.product.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(Decimal(response.data['price']), Decimal('999.99'))

    def test_product_update(self):
        data = {
            "price":1000, 
        }

        url = reverse('product-detail', args=(self.product.id,))

        old_price = self.product.price

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.product.refresh_from_db()
        self.assertEqual(self.product.price, old_price)


    def test_admin_can_update_product(self):
        self.user.is_staff = True
        self.user.save()
        data = {
            "price":1000
        }

        url = reverse('product-detail', args=(self.product.id,))
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_product_del(self):
        url = reverse('product-detail', args=(self.product.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_product_category(self):
        url = reverse('product-category-list', args=(self.product.category,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data['results'][0]['name'], 'Nike Jordans')


class CartAPITests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='jude', password='password123@')
        self.user2 = User.objects.create_user(username='simon', password='password123@')

        self.client.force_authenticate(user=self.user1)

        self.cart1 = Cart.objects.create(user=self.user1, status='PENDING')
        self.cart2 = Cart.objects.create(user=self.user1, status='CANCELLED')
        self.cart3 = Cart.objects.create(user=self.user2, status='PAID')


    def test_cart_create(self):
        data = {
            "user": self.user1,
            "status": "PAID"
        }

        url = reverse('cart-list')

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_pending_cart_does_not_create_if_pending_cart_already_exist(self):
        data = {
            "user": self.user1,
            "status": "PENDING"
        }

        url = reverse('cart-list')

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_cart_list_for_user1(self):
        url = reverse('cart-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        statuses = [cart['status'] for cart in response.data]
        self.assertIn('PENDING', statuses)


    def test_cart_list_for_user2(self):
        url = reverse('cart-list')
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['status'], 'PAID')


    def test_cart_individual(self):
        url = reverse('cart-detail', args=(self.cart2.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data['status'], 'CANCELLED')


    def test_cart_update(self):
        data = {
            "status": "PENDING"
        }
        url = reverse('cart-detail', args=(self.cart3.id,))
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.cart3.refresh_from_db()
        result = self.client.get(url)
        self.assertEqual(result.data['status'], 'PENDING')


    def test_cart_del(self):
        url = reverse('cart-detail', args=(self.cart1.id,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_pending_cart_get_or_create(self):
        url = reverse('pending-cart')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=self.user2)
        result = self.client.get(url)
        self.assertEqual(result.status_code, status.HTTP_200_OK)


class CartItemAPITests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='jude', password='password123@')
        self.user2 = User.objects.create_user(username='simon', password='password123@')

        self.client.force_authenticate(user=self.user1)

        self.cart1 = Cart.objects.create(user=self.user1, status='PENDING')
        self.cart2 = Cart.objects.create(user=self.user1, status='CANCELLED')
        self.cart3 = Cart.objects.create(user=self.user2, status='PAID')

        self.product1 = Product.objects.create(name='Nike Jordans', description='Kicks on air', price= Decimal('999.99'), category='FW')
        self.product2 = Product.objects.create(name='Hoody', description='Keeps you comfy', price= Decimal('100'), category='CL')

        self.cartItem1 = CartItem.objects.create(cart=self.cart1, product=self.product1, quantity=5)
        self.cartItem2 = CartItem.objects.create(cart=self.cart1, product=self.product2, quantity=10)
        self.cartItem3 = CartItem.objects.create(cart=self.cart3, product=self.product1, quantity=100)


    def test_cartItem_create(self):
        data = {
            "product": self.product2.id,
            "quantity": 6
        }

        url = reverse('item-list', args=(self.cart1.id,))
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_cartItem_list(self):
        url = reverse('item-list', args=(self.cart1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)

        url1 = reverse('cart-detail', args=(self.cart1.id,))
        result = self.client.get(url1)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertIsInstance(result.data, dict)
        self.assertEqual(result.data['total_price'], Decimal('5999.95'))


    def test_cartItem_inividual(self):
        url = reverse('item-detail', args=(self.cartItem1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url1 = reverse('item-detail', args=(self.cartItem3.id,))
        self.client.force_authenticate(user=self.user2)
        result = self.client.get(url1)
        self.assertEqual(result.status_code, status.HTTP_200_OK)


    def test_cartItem_update(self):
        data = {
            "quantity": 500
        }

        url = reverse('item-detail', args=(self.cartItem2.id,))
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_user_can_delete_cartItem_in_pending_cart(self):
        url = reverse('item-detail', args=(self.cartItem2.id,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_user_cannot_delete_cartItem_not_in_pending_cart(self):
        url = reverse('item-detail', args=(self.cartItem3.id,))
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)