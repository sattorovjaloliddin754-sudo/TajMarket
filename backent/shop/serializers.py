from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    # Формати вақт бо соат, дақиқа ва сония
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'price', 'description', 'image', 
            'status', 'location', 'phone', 'delivery', 
            'created_at', 'owner', 'owner_name', 'category', 'category_name'
        ]