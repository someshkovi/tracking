from django.urls import path
from products.views import index, ProductsListView, ProductDetailView, ProductUpdateView, ProductDeleteView

app_name = 'products'
urlpatterns = [
    path('', index, name='index'),
    path('all/', ProductsListView.as_view(), name='products-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
]
