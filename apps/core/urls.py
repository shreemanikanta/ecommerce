from django.urls import path
from apps.core.views import (
    CategoryListCreateAPIView, 
    CategoryRetrieveUpdateDestroyAPIView,
    ProductListCreateAPIView,
    ProductRetrieveUpdateDestroyAPIView,
    ProductApprovalView,
    MyProductsView)

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<uuid>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<uuid>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
    path('products/<uuid:uuid>/status/', ProductApprovalView.as_view(), name='product-status'),
    path("my-products/", MyProductsView.as_view(), name="my-products"),
]
