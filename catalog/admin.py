from django.contrib import admin
from .models import Product, Category, AttributeValue, ProductImage


class AttributeInline(admin.TabularInline):
    model = AttributeValue
    extra = 0

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [AttributeInline, ProductImageInline, ]

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass
