from rest_framework.views import APIView
from django.shortcuts import render
from apps.core.models import Category, Product
from apps.core.serializers import CategorySerializer, ProductSerializer
from rest_framework.permissions import IsAuthenticated
from apps.core.tasks import process_product_video
from utils.mixins import ResponseViewMixin
from utils.permissions import IsAdmin, IsStaff, IsAgent, IsAdminOrStaff
from utils.decorators import log_execution_time

class CategoryListCreateAPIView(APIView, ResponseViewMixin):
    """
    API view to handle listing and creation of categories.

    Methods:
        get(request):
            Retrieve a list of all categories.
            Returns a success response with serialized category data.

        post(request):
            Create a new category with the provided data.
            Returns a success response with the created category data if valid,
            otherwise returns an error response with validation errors.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return self.success_response(data=serializer.data, message="Fetched Successfully")

    @log_execution_time
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.success_response(data=serializer.data, message="Category created")
        return self.error_response(message="Validation failed", data=serializer.errors)


class CategoryRetrieveUpdateDestroyAPIView(APIView, ResponseViewMixin):
    """
    This View handles the retrieval, update, and deletion of a Category object.

    This API view supports the following HTTP methods:
    - GET: Retrieve the details of a specific category by its UUID.
    - PATCH: Partially update the details of a specific category by its UUID.
    - DELETE: Delete a specific category by its UUID.
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, uuid):
        return Category.objects.filter(uuid=uuid).first()

    def get(self, request, uuid):
        category = self.get_object(uuid)
        if not category:
            return self.error_response(message="Category not found")
        serializer = CategorySerializer(category)
        return self.success_response(data=serializer.data, message="Category details fetched")

    def patch(self, request, uuid):
        category = self.get_object(uuid)
        if not category:
            return self.error_response(message="Category not found")
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.success_response(data=serializer.data, message="Category updated")
        return self.error_response(message="Update failed", data=serializer.errors)

    def delete(self, request, uuid):
        category = self.get_object(uuid)
        if not category:
            return self.error_response(message="Category not found")
        category.delete()
        return self.success_response(message="Category deleted")


class ProductListCreateAPIView(APIView, ResponseViewMixin):

    """
    API view to handle listing and creation of products.

    This view provides two main functionalities:
    1. GET: Retrieve a list of all products along with their associated categories.
    2. POST: Create a new product with the provided data.
    """
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
    """
    This View handles retrieving, updating, and deleting a product.

    Methods:
        get_object(uuid):
            Retrieves a product instance by its UUID.

        get(request, uuid):
            Retrieves a product by UUID and returns its serialized data.
            Returns an error response if the product is not found.

        patch(request, uuid):
            Partially updates a product by UUID with the provided data.
            Triggers video processing if a video is updated.
            Returns an error response if the product is not found or the update fails.

        delete(request, uuid):
            Deletes a product by UUID.
            Returns an error response if the product is not found.
    """
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
            return self.error_response(message="Product not found")
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
            return self.error_response(message="Product not found")
        product.delete()
        return self.success_response(message="Product deleted")


class ProductApprovalView(APIView, ResponseViewMixin):
    """
    View to handle product approval or rejection by admin or staff.

    This view allows authenticated admin or staff users to approve or reject
    a product based on its UUID. The action is specified in the request data.
    """
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

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
    """
    View to retrieve the list of products uploaded by the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.filter(created_by=request.user)
        serializer = ProductSerializer(products, many=True)
        return self.success_response(data=serializer.data, message="Your uploaded products")
    

def dashboard_view(request):
    """Dashboard Page"""
    return render(request, 'core/dashboard.html')

def categories_view(request):
    """Categories management page"""
    return render(request, 'core/categories.html')

def products_view(request):
    """Products management page"""
    return render(request, 'core/products.html')


def my_products_view(request):
    """User's own products page"""
    return render(request, 'core/my_products.html')

def orders_view(request):
    """Orders management page"""
    return render(request, 'core/orders.html')

def order_detail_view(request, uuid):
    """Individual order detail page"""
    context = {'order_uuid': uuid}
    return render(request, 'core/order_detail.html', context)

# Admin/Staff Only Views
def product_approval_view(request):
    """Product approval page for staff/admin"""
    return render(request, 'core/product_approval.html')


def generate_products_view(request):
    """Generate dummy products page (admin only)"""
    return render(request, 'core/generate_products.html')

def export_products_view(request):
    """Export products page (admin only)"""
    return render(request, 'core/export_products.html')


