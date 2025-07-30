from django.urls import path
from apps.core.views import (
    CategoryListCreateAPIView, 
    CategoryRetrieveUpdateDestroyAPIView,
    ProductListCreateAPIView,
    ProductRetrieveUpdateDestroyAPIView,
    ProductApprovalView,
    MyProductsView,
    dashboard_view)
from apps.core import views

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<uuid>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<uuid>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
    path('products/<uuid:uuid>/status/', ProductApprovalView.as_view(), name='product-status'),
    path("my-products/", MyProductsView.as_view(), name="my-products"),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('', views.dashboard_view, name='dashboard'),
    path('categories_page/', views.categories_view, name='categories'),
    path('products_page/', views.products_view, name='products'),
    path('my-products_page/', views.my_products_view, name='my_products'),
    path('orders/', views.orders_view, name='orders'),
    path('orders/<uuid:uuid>/', views.order_detail_view, name='order_detail'),
    # Admin/Staff Pages
    path('product-approval/', views.product_approval_view, name='product_approval'),
    path('generate-products/', views.generate_products_view, name='generate_products'),
    path('export-products/', views.export_products_view, name='export_products'),
    
]
