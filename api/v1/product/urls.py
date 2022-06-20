from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductsAPI.as_view()),
    path('<int:pk>/', views.ProductRetrieveUpdateDestroyAPI.as_view()),
    path('update/<int:pk>/', views.fetch_latest_price),
]
