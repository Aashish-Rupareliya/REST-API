from rest_framework import serializers
from .models import Customer, Product, Order, OrderItem
from django.utils import timezone

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_weight(self, value):
        if value <= 0 or value > 25:
            raise serializers.ValidationError("Weight must be positive and not more than 25kg.")
        return value

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']  

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)  

    class Meta:
        model = Order
        fields = ['order_number', 'order_date', 'address', 'customer', 'order_items']  

    def validate_order_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Order date cannot be in the past.")
        return value

    def validate(self, data):
        total_weight = sum(item['product'].weight * item['quantity'] for item in data['order_items'])
        if total_weight > 150:
            raise serializers.ValidationError("Order cumulative weight must be under 150kg.")
        return data

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for order_item_data in order_items_data:
            OrderItem.objects.create(order=order, **order_item_data)
        return order
