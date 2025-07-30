from rest_framework import serializers
from apps.core.models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['uuid', 'name', 'description', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['uuid', 'name', 'description', 'category', 'price', 'stock', 'is_active', 'status', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_by']
