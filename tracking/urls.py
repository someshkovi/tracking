"""tracking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include


def test(request):
    return render(request, 'test-table2.html', {})


def index(request):
    context = {}
    return render(request, 'index.html', context)


from accounts.views import SignUpView
from products.views import index

urlpatterns = [
    path('', index, name='index'),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # path('exercise/', include('exercise.urls')),
    path('products/', include('products.urls')),
    path('test/', test, name='test')
]
