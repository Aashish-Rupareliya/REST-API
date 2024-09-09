from django.shortcuts import render
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from .models import Order
from .serializers import OrderSerializer
from .serializers import ProductSerializer, CustomerSerializer, OrderSerializer, OrderItemSerializer

from rest_framework import viewsets
from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        products = self.request.query_params.get('products')
        customer = self.request.query_params.get('customer')
        if products:
            product_list = products.split(',')
            queryset = queryset.filter(orderitem__product__name__in=product_list).distinct()
        if customer:
            queryset = queryset.filter(customer__name=customer)
        return queryset