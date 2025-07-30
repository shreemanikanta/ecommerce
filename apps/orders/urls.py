from django.urls import path
from apps.orders.views import CreateOrderView, OrderListView, OrderDetailView

urlpatterns = [
    path("create/", CreateOrderView.as_view(), name="create-order"),
    path('', OrderListView.as_view(), name='order-list'),
    path('<uuid:uuid>/', OrderDetailView.as_view(), name='order-detail'),
]
