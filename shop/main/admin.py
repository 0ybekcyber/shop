from django.contrib import admin
from .models import Category, Product, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'added_at', 'is_new')
    list_filter = ('category', 'is_new')
    search_fields = ('name', 'description')
    ordering = ('-added_at',)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'text', 'created_at')
    list_filter = ('created_at', 'user', 'product')
    search_fields = ('text', 'user__username', 'product__name')

