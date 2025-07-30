from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from apps.orders.models import Order, OrderItem
from apps.core.models import Product
from utils.mixins import ResponseViewMixin
from apps.orders.serializers import OrderCreateSerializer, OrderSerializer, OrderItemSerializer

class CreateOrderView(APIView, ResponseViewMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return self.error_response(data=serializer.errors, message="Validation failed")

        try:
            with transaction.atomic():
                order = Order.objects.create(user=request.user)

                for item in serializer.validated_data["items"]:
                    product = Product.objects.get(uuid=item["product_uuid"])
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item["quantity"],
                        price_at_order=product.price
                    )

        except Product.DoesNotExist:
            return self.error_response(message="One or more products not found")

        return self.success_response(message="Order placed successfully", data=serializer.data)
    
class OrderListView(APIView, ResponseViewMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related("items__product")
        serializer = OrderSerializer(orders, many=True)
        return self.success_response(data=serializer.data, message="Orders fetched")
    
class OrderDetailView(APIView, ResponseViewMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid):
        try:
            order = Order.objects.prefetch_related("items__product").get(uuid=uuid, user=request.user)
        except Order.DoesNotExist:
            return self.error_response(message="Order not found", status_code=404)
        serializer = OrderSerializer(order)
        return self.success_response(data=serializer.data, message="Order detail fetched")
