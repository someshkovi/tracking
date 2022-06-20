import json

from django.http import HttpResponse, JsonResponse
from django.http.request import QueryDict
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models.signals import post_save
from rest_framework_simplejwt.authentication import JWTAuthentication

from products.models import Product
from . import serializers
from . import signals
from scripts.fetch_data import store_update_price


class ProductsAPI(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer

    # permission_classes = (AllowAny, )

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.ProductSerializer(queryset, many=True)
        return Response({
            'status': True,
            'count': len(serializer.data),
            'data': serializer.data,
        })

    def create(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, QueryDict):
            data = request.data.dict()
        if data.get('url') is not None:
            response = json.loads(store_update_price(data.get('url')))
            if response.get('price') is not None:
                data['price'] = response.get('price')
            if (data.get('name') is None or data.get('name') == '') and response.get('name') is not None:
                data['name'] = response.get('title')[:200]
            data['is_url_valid'] = response.get('is_url_valid')
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response({
            "status": True,
            "message": "Product Added!",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)


class ProductRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(id=self.kwargs.get('pk', None))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({
            "status": True,
            "message": "Product Updated !",
            "data": serializer.data
        })


@csrf_exempt
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def fetch_latest_price(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return HttpResponse(status=404)
    if product.url is not None:
        response = json.loads(store_update_price(product.url))
        price = response.get('price')
        if price is not None:
            product.price = price
            # updating min price
            if product.min_price is None:
                product.min_price = price
            if product.min_price < price:
                product.min_price = price
            # updating max price
            if product.max_price is None:
                product.max_price = price
            if product.max_price > price:
                product.max_price = price

        if (product.name is None or product.name == '') and response.get('name') is not None:
            product.name = response.get('title')[:200]
        product.is_url_valid = response.get('is_url_valid')
    serializer = serializers.ProductSerializer(product)
    product.save()
    return JsonResponse(serializer.data, status=201)