from celery import shared_task
from apps.core.models import Product

@shared_task
def process_product_video(uuid):
    try:
        product = Product.objects.get(uuid=uuid)
        print(f"[Celery] Processing video for product: {product.name}")
        # Simulate processing
    except Product.DoesNotExist:
        print("[Celery] Product not found")
