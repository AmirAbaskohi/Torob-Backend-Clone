from django.shortcuts import render
from .models import Category, Product, Shop, ProductPrice, ProductFeature
from .serializers import CategorySerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.core.paginator import Paginator
import pandas as pd
from .utils import generate_uuid
from datetime import datetime
import os
import requests

class GetCategoriesView(APIView):
    serializer_class = CategorySerializer
    lookup_url_page = 'page'
    lookup_url_size = 'size'

    def get(self, request, format=None):
        page = request.GET.get(self.lookup_url_page)
        if page == None:
            page = 1
        size = request.GET.get(self.lookup_url_size)
        if size == None:
            size = 10

        page = int(page)
        size = int(size)

        categories = Category.objects.all()
        paginator = Paginator(categories, size)

        if page not in paginator.page_range:
            return Response({"error": "Invalid page number"}, status=status.HTTP_400_BAD_REQUEST)
        paged_categories = paginator.page(page)

        next, prev = "", ""
        if page+1 in paginator.page_range:
            next = f"/category/list?page={page+1}&size={size}"
        else:
            next = None
        if page == 1:
            prev = None
        else:
            prev = f"/category/list?page={page-1}&size={size}"

        data = CategorySerializer(paged_categories, many=True).data
        response = { 
            'next': next,
            "prev": prev,
            "count": paginator.count,
            "results": data
        }
        return Response(response, status=status.HTTP_200_OK)

class ProductCreateOrUpdateView(APIView):
    def get_suggestion(self, suggestion_url, product):
        features = ProductFeature.objects.filter(product_id=product).all()
        request_body = { 'name': product.name, 'features': dict() }
        for feature in features:
            request_body['features'][feature.feature_name] = feature_value
        response = requests.post(suggestion_url, json=request_body)
        return response.json()['id']

    def add_category(self, product):
        suggestion_url = os.environ['SUGGESTOIN_BASE_URL']
        category = Category.objects.filter(id=self.get_suggestion(suggestion_url, product)).first()
        product.categories.add(category)
        product.save()

    def update_product(self, data, product):
        if data['is_available']:
            product.price = data['price']
        else:
            product.price = None
        product.updated = datetime.now()
        product.save()
        new_price = ProductPrice(price=data['price'], product_id=product)
        new_price.save()
        for key, value in data['features'].items():
            feature = ProductFeature.objects.filter(product_id=product.id, feature_name=key).first()
            if feature == None:
                feature = ProductFeature(product_id=product, feature_name=key, feature_value=value)
                feature.save()
            else:
                feature.feature_value = value
                feature.save()

    def create_product(self, data, shop):
        if data['is_available']:
            price = data['price']
        else:
            price = None
        product = Product(name=data['name'],uuid=generate_uuid(), url=data['page_url'], price=price, shop_id=shop, updated=datetime.now())
        product.save()
        new_price = ProductPrice(price=data['price'], product_id=product)
        new_price.save()
        for key, value in data['features'].items():
            feature = ProductFeature.objects.filter(product_id=product.id, feature_name=key).first()
            feature = ProductFeature(product_id=product, feature_name=key, feature_value=value)
            feature.save()
        self.add_category(product)

    def post(self, request, format=None):
        shop = Shop.objects.filter(domain=request.data['shop_domain']).first()
        if shop == None:
            return Response({'Error': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)
        product = Product.objects.filter(name=request.data['name'], shop_id=shop.id).first()
        if product == None:
            self.create_product(request.data, shop)
            return Response({'Response': 'Created Successfully'}, status=status.HTTP_201_CREATED)
        else:
            self.update_product(request.data, product)
            return Response({'Response': 'Updated Successfully'}, status=status.HTTP_200_OK)