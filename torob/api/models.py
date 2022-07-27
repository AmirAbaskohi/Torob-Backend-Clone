from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100)
    level = models.PositiveSmallIntegerField()
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Category => Id: {self.id}, Title: {self.title}, Level: {self.level}, Parent: {self.parent_id}"

class Shop(models.Model):
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100, default="NotFound")

    def __str__(self):
        return f"Shop => Id: {self.id}, Name: {self.name}, Domain: {self.domain}"

class Product(models.Model):
    uuid = models.CharField(max_length=12)
    name = models.CharField(max_length=100)
    updated = models.DateTimeField()
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE, null=False, blank=False)
    price = models.PositiveIntegerField(blank=True, null=True)
    categories = models.ManyToManyField(Category)
    url = models.CharField(max_length=100, default="NotFound")

    def __str__(self):
        return f"Product => Id: {self.id}, Name: {self.name}, UUID: {self.uuid}, Updated: {self.updated}, Price: {self.price}, Categories: {self.categories}, Shop: {self.shop_id}, URL: {self.url}"

class ProductPrice(models.Model):
    price = models.PositiveIntegerField(blank=True, null=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"Product Price => Id: {self.id}, Price: {self.price}, Product: {self.product_id}"

class ProductFeature(models.Model):
    feature_name = models.CharField(max_length=100)
    feature_value = models.CharField(max_length=100)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"Product Feature => Id: {self.id}, Feature Name: {self.feature_name}, Feature Value: {self.feature_value}, Product: {self.product_id}"
