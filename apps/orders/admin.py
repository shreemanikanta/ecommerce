from django.contrib import admin
from apps.orders.models import Order, OrderItem
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "user",
    ]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "order",
        "product",
        "quantity",    
        "price_at_order",
    ]