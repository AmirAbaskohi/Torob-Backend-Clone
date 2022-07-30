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
    price = serializers.SerializerMethodField('get_product_price')
    shop_name = serializers.CharField(source='shop_id.name')
    updated = serializers.SerializerMethodField('get_updated')
    uid = serializers.CharField(source='uuid')

    def get_product_redirect_url(self, product):
        return f"/product/redirect/?uid={product.uuid}"

    def get_product_price(self, product):
        if product.price == None:
            return None
        return f"{product.price} تومان"

    def get_product_price_list_url(self, product):
        return f"/product/price-change/list/?uid={product.uuid}"

    def get_updated(self, product):
        return f"{int((datetime.now(timezone.utc)-product.updated).total_seconds()//60)} دقیقه پیش"

    class Meta:
        model = Product
        fields = [
            'uid', 'name',
            'shop_name', 'product_redirect_url',
            'product_price_list_url',
            'updated', 'is_available'
        ]

class ProductPriceSerializer(serializers.ModelSerializer):
    old_price = serializers.SerializerMethodField('get_old_product_price')
    new_price = serializers.SerializerMethodField('get_new_product_price')
    price_change_time = serializers.SerializerMethodField('get_created')

    def get_old_product_price(self, product_price):
        if product_price.old_price == None:
            return None
        return f"{product_price.old_price} تومان"

    def get_new_product_price(self, product_price):
        if product_price.new_price == None:
            return None
        return f"{product_price.new_price} تومان"

    def get_created(self, product_price):
        return f"{int((datetime.now(timezone.utc)-product_price.created_at).total_seconds()//60)} دقیقه پیش"

    class Meta:
        model = Product
        fields = ['new_availability', 'new_price', 'old_price', 'old_availability', 'price_change_time']