from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Category
from collections import OrderedDict

class TestGetCategoryList(APITestCase):
    def setUp(self):
        self.category1 = Category.objects.create(title='phone and tablet', level=1, parent_id=None)
        self.category2 = Category.objects.create(title='computer', level=1, parent_id=None)
        self.category3 = Category.objects.create(title='tablet', level=2, parent_id=self.category1)

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