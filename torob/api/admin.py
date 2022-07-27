from django.contrib import admin
from .models import Category, ProductPrice, Product, Shop, ProductFeature

admin.site.register(Category)
admin.site.register(ProductPrice)
admin.site.register(Product)
admin.site.register(Shop)
admin.site.register(ProductFeature)
