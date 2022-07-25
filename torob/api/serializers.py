from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    level = serializers.IntegerField()
    parent_category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Category
        fields = "__all__"
