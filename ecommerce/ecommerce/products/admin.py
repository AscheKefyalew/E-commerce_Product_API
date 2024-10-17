from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Brand, Category, Product, ProductImage, Attribute, AttributeValue, ProductType, ProductAttributeValue

# Helper for adding edit links
class EditLinkInline(object):
    def edit(self, instance):
        url = reverse(f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change", args=[instance.pk],)
        if instance.pk:
            link = mark_safe('<a href="{u}">edit</a>'.format(u=url))
            return link
        else:
            return ""

# Inline for managing product images
class ProductImageInline(admin.TabularInline):
    model = ProductImage

# Inline for managing attribute values directly from Product
class AttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue  # Use the through model directly
    extra = 1  # Optional: Set the number of empty forms to display

# Admin configuration for Product
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, AttributeValueInline]  # Show images and attribute values in the product form

# Inline for Attribute and ProductType relationship
class AttributeInline(admin.TabularInline):
    model = Attribute.product_type_attribute.through  # Use the through table for the relation

# Admin configuration for ProductType
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        AttributeInline,
    ]

# Register models with the updated admin configurations
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Attribute)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(AttributeValue)
