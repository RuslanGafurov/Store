from django.contrib import admin

from products.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Расширенное отображение категорий"""
    list_display = ('name', 'description')
    fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Расширенное отображение товаров"""
    list_display = ('name', 'category', 'price', 'quantity')
    fields = ('name', 'category', 'image', 'description', ('quantity', 'price'))
    ordering = ('name',)
