from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.core.models import Category, Product
from apps.core.serializers import CategorySerializer, ProductSerializer
from rest_framework.permissions import IsAuthenticated
from apps.core.tasks import process_product_video
from utils.mixins import ResponseViewMixin
from utils.permissions import IsAdmin, IsStaff


class CategoryListCreateAPIView(APIView, ResponseViewMixin):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return self.success_response(data=serializer.data, message="Fetched Successfully")

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.success_response(data=serializer.data, message="Category created")
        return self.error_response(message="Validation failed", data=serializer.errors)


class CategoryRetrieveUpdateDestroyAPIView(APIView, ResponseViewMixin):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, uuid):
        return Category.objects.filter(uuid=uuid).first()

    def get(self, request, uuid):
        category = self.get_object(uuid)
        if not category:
            return self.error_response(message="Category not found", status_code=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return self.success_response(data=serializer.data, message="Category details fetched")

    def patch(self, request, uuid):
        category = self.get_object(uuid)
        if not category:
            return self.error_response(message="Category not found", status_code=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.success_response(data=serializer.data, message="Category updated")
        return self.error_response(message="Update failed", data=serializer.errors)

    def delete(self, request, uuid):
        category = self.get_object(uuid)
        if not category:
            return self.error_response(message="Category not found", status_code=status.HTTP_404_NOT_FOUND)
        category.delete()
        return self.success_response(message="Category deleted")


class ProductListCreateAPIView(APIView, ResponseViewMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products, many=True)
        return self.success_response(data=serializer.data)

    def post(self, request):
        category_uuid = request.data.get("category")
        try:
            category = Category.objects.get(uuid=category_uuid)
        except Category.DoesNotExist:
            return self.error_response(message="Invalid category UUID", status_code=400)
        data = request.data.copy()
        data["category"] = category.id
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            product = serializer.save(created_by=request.user)
            if product.video:
                process_product_video.delay(str(product.uuid))
            return self.success_response(data=serializer.data, message="Product created")
        return self.error_response(message="Validation failed", data=serializer.errors)


class ProductRetrieveUpdateDestroyAPIView(APIView, ResponseViewMixin):
    permission_classes = [IsAuthenticated]

    def get_object(self, uuid):
        return Product.objects.filter(uuid=uuid).first()

    def get(self, request, uuid):
        product = self.get_object(uuid)
        if not product:
            return self.error_response(message="Product not found")
        serializer = ProductSerializer(product)
        return self.success_response(data=serializer.data)

    def patch(self, request, uuid):
        product = self.get_object(uuid)
        if not product:
            return self.error_response(message="Product not found", status_code=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            updated_product = serializer.save()
            if 'video' in request.data and updated_product.video:
                process_product_video.delay(str(updated_product.uuid))
            return self.success_response(data=serializer.data, message="Product updated")
        return self.error_response(message="Update failed", data=serializer.errors)

    def delete(self, request, uuid):
        product = self.get_object(uuid)
        if not product:
            return self.error_response(message="Product not found", status_code=status.HTTP_404_NOT_FOUND)
        product.delete()
        return self.success_response(message="Product deleted")


class ProductApprovalView(APIView, ResponseViewMixin):
    permission_classes = [IsAuthenticated, IsStaff]

    def post(self, request, uuid):
        action = request.data.get("action")  
        if action not in ["approve", "reject"]:
            return self.error_response(message="Invalid action")

        try:
            product = Product.objects.get(uuid=uuid)
        except Product.DoesNotExist:
            return self.error_response(message="Product not found")

        product.status = "approved" if action == "approve" else "rejected"
        product.save()

        return self.success_response(message=f"Product {action}ed successfully")
    
class MyProductsView(APIView, ResponseViewMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.filter(created_by=request.user)
        serializer = ProductSerializer(products, many=True)
        return self.success_response(data=serializer.data, message="Your uploaded products")
