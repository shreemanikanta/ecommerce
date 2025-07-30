from django.contrib import admin
from apps.core.models import Category, Product
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "name",
        "description",
        "created_at",    
        "updated_at",
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "name",
        "description",
        "category",
        "price",
        "stock",
        "is_active",
        "status",
        "created_by",
        "created_at",    
        "updated_at",
    ]