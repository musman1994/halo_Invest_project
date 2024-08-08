import requests
import csv
import os
from django.db.models import Sum, F
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import authenticate, login, logout
from .serializers import StockSerializer, OrderSerializer
from configparser import ConfigParser
from django.conf import settings
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from trading.models import Stock, Order
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User


class StockListCreateView(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class UserStockValueView(generics.GenericAPIView):

    def get(self, request, stock_id):
        try:
            stock = Stock.objects.get(id=stock_id)
        except Stock.DoesNotExist:
            return Response({'error': 'Stock not found'}, status=404)

        user = request.user

        # Calculate total investment
        total_investment = Order.objects.filter(
            user=user,
            stock=stock,
            trade_type='buy'
        ).aggregate(
            total=Sum(F('quantity') * F('stock__price'))
        )['total'] or 0

        return Response({'Total Investment($)': total_investment})


class PlaceTradesInBulk(APIView):
    permission_classes = [AllowAny]  # Allow any user to call this endpoint

    def get_config(self, filename, section='auth'):
        """Read the config file and return the auth credentials."""
        parser = ConfigParser()
        parser.read(filename)

        if parser.has_section(section):
            return {key: parser.get(section, key) for key in parser.options(section)}
        else:
            raise Exception(f'Section {section} not found in the {filename} file')

    def get_jwt_token(self, username, password):
        """Obtain JWT token from the Django API."""
        TOKEN_URL = "http://127.0.0.1:8000/api/token/"
        response = requests.post(TOKEN_URL, json={"username": username, "password": password})
        if response.status_code == 200:
            return response.json().get("access")
        else:
            raise Exception(f"Failed to obtain JWT token: {response.json()}")

    def get_user_from_token(self, token):
        """Get the user instance from the JWT token."""
        access_token = AccessToken(token)
        user_id = access_token["user_id"]
        return User.objects.get(id=user_id)

    def post(self, request, *args, **kwargs):
        # Step 1: Read credentials from config file
        try:
            config_file_path = os.path.join(settings.BASE_DIR, 'config.ini')
            credentials = self.get_config(config_file_path)
            username = credentials['username']
            password = credentials['password']
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        # Step 2: Obtain JWT Token
        try:
            access_token = self.get_jwt_token(username, password)
            user = self.get_user_from_token(access_token)  # Get user instance from token
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=401)

        # Step 3: Process CSV file and create orders
        csv_file_path = os.path.join(settings.BASE_DIR, 'data.csv')

        if not os.path.exists(csv_file_path):
            return JsonResponse({'error': 'CSV file not found'}, status=404)

        orders = []
        try:
            with open(csv_file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    stock_id = row['stock_id']
                    quantity = int(row['quantity'])
                    trade_type = row['trade_type']

                    try:
                        stock = Stock.objects.get(id=stock_id)
                        orders.append(Order(
                            user=user,  # Use the correct user instance
                            stock=stock,
                            quantity=quantity,
                            trade_type=trade_type
                        ))
                    except ObjectDoesNotExist:
                        return JsonResponse({'error': f'Stock with ID {stock_id} does not exist'}, status=404)

                if orders:
                    Order.objects.bulk_create(orders)
                    return JsonResponse({'message': f'Successfully imported {len(orders)} trades'}, status=200)
                else:
                    return JsonResponse({'message': 'No valid trades to import'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
