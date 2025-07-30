from rest_framework import serializers
from apps.orders.models import Order, OrderItem
from apps.core.models import Product

class OrderItemCreateSerializer(serializers.Serializer):
    product_uuid = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)

class OrderCreateSerializer(serializers.Serializer):
    items = OrderItemCreateSerializer(many=True)

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must have at least one item.")
        return value

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ['uuid', 'product', 'product_name', 'quantity', 'price_at_order']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['uuid', 'user', 'created_at', 'updated_at', 'items']