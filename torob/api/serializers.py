from rest_framework import serializers
from .models import Category, Product
from datetime import datetime, timezone

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'parent_id']

class ProductSerializer(serializers.ModelSerializer):
    product_redirect_url = serializers.SerializerMethodField('get_product_redirect_url')
    product_price_list_url = serializers.SerializerMethodField('get_product_price_list_url')
    shop_name = serializers.CharField(source='shop_id.name')
    is_available = serializers.SerializerMethodField('is_available')
    updated = serializers.SerializerMethodField('get_updated')
    uid = serializers.CharField(source='uuid')

    def get_product_redirect_url(self, product):
        return f"/product/redirect/?uid={product.uuid}"

    def get_product_price_list_url(self, product):
        return f"/product/price-change/list/?uid={product.uuid}"

    def is_available(self, product):
        return product.price == None

    def get_updated(self, product):
        return f"{int((datetime.now(timezone.utc)-product.updated).total_seconds()//60)} دقیقه پیش"

    class Meta:
        model = Product
        fields = [
            'uid', 'name', 'price',
            'shop_name', 'product_redirect_url',
            'product_price_list_url',
            'updated'
        ]