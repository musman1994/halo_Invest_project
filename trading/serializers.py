from rest_framework import serializers
from .models import Stock, Order


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'name', 'price']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'stock', 'trade_type', 'quantity', 'timestamp']

