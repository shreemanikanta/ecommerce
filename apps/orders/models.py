from django.db import models
from apps.users.models import AppUser as User
from apps.core.models import Product
from utils.models import TimeStampModel
import uuid

# Create your models here.
class Order(TimeStampModel):
    """
    Order model represents a customer's order, including the user who placed it.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class OrderItem(TimeStampModel):
    """
    OrderItem model represents an item in an order, including product details, quantity, and price at the time of order.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)
