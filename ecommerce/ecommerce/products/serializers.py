from rest_framework import serializers
from .models import Brand, Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = "__all__"
    
    def validate(self, data):
        if data['price'] <= 0:
            raise serializers.ValidationError("Price must be greater than zero")
        if data['stock_quantity'] < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative")
        return data