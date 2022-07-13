from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductsAPI.as_view(), name='product-list'),
    path('<int:pk>/', views.ProductRetrieveUpdateDestroyAPI.as_view(), name='product-detail-update-destroy'),
    path('update/<int:pk>/', views.fetch_latest_price, name='product-fetch-latest-price'),
    path('update/all/', views.UpdateAllMyProducts.as_view(), name='update-all-my-products-from-urls'),
    path('admin/update/all/', views.UpdateAllProducts.as_view(), name='update-all-products-from-urls'),
    path('pbtp/', views.GetProductsBelowTargetPrice.as_view(), name='products-below-target-price'),
]
