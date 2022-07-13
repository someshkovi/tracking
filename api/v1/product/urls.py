from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductsAPI.as_view(), name='product-list'),
    path('<int:pk>/', views.ProductRetrieveUpdateDestroyAPI.as_view(), name='product-detail-update-destroy'),
    path('update/<int:pk>/', views.fetch_latest_price, name='product-fetch-latest-price'),
    path('update/all/', views.fetch_latest_price_all_products, name='all-products-fetch-latest-price'),
]
