from rest_framework import serializers
from .models import Brand, Category, Product, ProductImage, Attribute, AttributeValue
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="name")

    class Meta:
        model = Category
        fields = ["category_name",]  # Change display name to 'category_name'

# Brand Serializer
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ("id",)  # Exclude the 'id' field

# Product Image Serializer
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('alternative_text', 'url', 'order')

# Attribute Serializer
class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ("name", "id")

# Attribute Value Serializer
class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields = (
            "attribute",
            "attribute_value",
        )

# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source="brand.name")
    category_name = serializers.CharField(source="category.name")
    product_image = ProductImageSerializer(many=True)
    attribute_value = AttributeValueSerializer(many=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "name",
            "description",
            "brand_name",
            "category_name",
            "price",  # Added price directly to Product
            "sku",    # Added SKU directly to Product
            "stock_qty",  # Added stock_qty directly to Product
            "product_image",  # Added product_image
            "attribute_value",  # Added attribute_value directly to Product
            "created_at",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Custom representation for attributes
        attr_data = data.pop("attribute_value", [])
        attribute_values = {}

        for item in attr_data:
            attribute_values[item['attribute']['name']] = item['attribute_value']

        data.update({"specification": attribute_values})

        return data
