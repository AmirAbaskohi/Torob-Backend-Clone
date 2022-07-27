from django.shortcuts import render
from .models import Category, Product, Shop, ProductPrice, ProductFeature
from .serializers import CategorySerializer, ProductSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.core.paginator import Paginator
from .utils import generate_uuid
from datetime import datetime, timezone
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
            request_body['features'][feature.feature_name] = feature.feature_value
        response = requests.post(suggestion_url+'product/create-or-update/', json=request_body)
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
        product.updated = datetime.now(timezone.utc)
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
        product = Product(name=data['name'],uuid=generate_uuid(), url=data['page_url'], price=price, shop_id=shop, updated=datetime.now(timezone.utc))
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

class GetProductListView(APIView):
    lookup_url_page = 'page'
    lookup_url_size = 'size'
    lookup_url_sort = 'sort'
    lookup_url_is_available = 'is_available'
    lookup_url_price_gt = 'price__gt'
    lookup_url_price_lt = 'price__lt'
    lookup_url_category_id = 'category_id'

    def get_wanted_categories(self, category):
        wanted_categories = [category.id]
        level = category.level
        while level < 3:
            wanted_categories.extend(list(Category.objects.filter(parent_id__in=wanted_categories, level=level+1).values_list('id', flat=True)))
            level += 1
        return wanted_categories

    def get_products(self, wanted_categories, sort):
        order_by_dict = {
            'price-': '-price',
            'price': 'price',
            'date_updated': 'updated',
            'date_updated-': '-updated'
        }
        if sort in order_by_dict.keys():
            order_by_value = order_by_dict[sort] 
        else:
            order_by_value = '-updated'
        

        return Product.objects.filter(categories__in=wanted_categories).order_by(order_by_value)

    def get(self, request, format=None):
        page = request.GET.get(self.lookup_url_page)
        if page == None:
            page = 1
        size = request.GET.get(self.lookup_url_size)
        if size == None:
            size = 10
        sort = request.GET.get(self.lookup_url_sort)
        if sort == None:
            sort = 'date_updated-'

        category_id = request.GET.get(self.lookup_url_category_id)
        if category_id == None:
            return Response({'Error': 'Category is not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        page = int(page)
        size = int(size)
        category_id = int(category_id)

        category = Category.objects.filter(id=category_id).first()
        if category == None:
            return Response({'Error': 'Category is not found'}, HTTP_404_NOT_FOUND)
        wanted_categories = self.get_wanted_categories(category)

        products = self.get_products(wanted_categories, sort)

        paginator = Paginator(products, size)
        if page not in paginator.page_range:
            return Response({"error": "Invalid page number"}, status=status.HTTP_400_BAD_REQUEST)
        paged_products = paginator.page(page)

        data = ProductSerializer(paged_products, many=True).data
        response = { 
            "results": data
        }
        return Response(response, status=status.HTTP_200_OK)