from django.contrib import admin
from .models import Stock, Order


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'stock', 'quantity', 'trade_type', 'timestamp')
