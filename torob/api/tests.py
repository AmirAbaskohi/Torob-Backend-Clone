from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Category, Product, Shop, ProductPrice, ProductFeature
from collections import OrderedDict
from .utils import generate_uuid 
import mock
from datetime import datetime

class TestGetCategoryList(APITestCase):
    def setUp(self):
        self.category1 = Category.objects.create(id=1, title='phone and tablet', level=1, parent_id=None)
        self.category2 = Category.objects.create(id=2, title='computer', level=1, parent_id=None)
        self.category3 = Category.objects.create(id=3, title='tablet', level=2, parent_id=self.category1)

    def test_get_categories(self):
        request = { 'page' : '2', 'size': '1'}
        response = self.client.get(reverse('categories'), request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['next'], "/category/list?page=3&size=1")
        self.assertEqual(response.data['prev'], "/category/list?page=1&size=1")
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(response.data['results'], [OrderedDict([('id', 2), ('title', 'computer'), ('parent_id', None)])])

    def test_get_invalid_page_categories(self):
        request = { 'page' : '5', 'size': '1'}
        response = self.client.get(reverse('categories'), request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestCreateOrUpdateProduct(APITestCase):
    def setUp(self):
        self.category1 = Category.objects.create(title='phone and tablet', level=1, parent_id=None)
        self.category2 = Category.objects.create(title='phone', level=2, parent_id=self.category1)
        self.category3 = Category.objects.create(title='samsung', level=3, parent_id=self.category2)
        self.shop = Shop.objects.create(name='digikala', domain='some_domain')
        self.product = Product.objects.create(name='a30',uuid=generate_uuid(), url='some_url', price=1000, shop_id=self.shop, updated=datetime.now())

    @mock.patch('api.views.ProductCreateOrUpdateView.get_suggestion', side_effect=[None, 3])
    def test_create_product(self, mocked_get_suggestion):
        request = {
            "page_url": "http://digikala.com/DKP-1213",
            "shop_domain": "some_domain",
            "name": "موبایل آیفون xs max 64Gb",
            "price": 12000000,
            "is_available": True,
            "features": {
                "حافظه": "24 Gb"
            }
        }
        response = self.client.post(reverse('productcreate'), request, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.last().price, 12000000)

    def test_update_product(self):
        request = {
            "page_url": "some_url",
            "shop_domain": "some_domain",
            "name": "a30",
            "price": 2000,
            "is_available": True,
            "features": {
                "حافظه": "24 Gb"
            }
        }
        response = self.client.post(reverse('productcreate'), request, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.first().price, 2000)