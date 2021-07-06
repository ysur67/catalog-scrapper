from django.contrib import admin
from .models import Product, Category, AttributeValue


class AttributeInline(admin.TabularInline):
    model = AttributeValue
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [AttributeInline, ]

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    pass
