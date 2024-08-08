import pytest
import requests

# Base URL of your Django API
BASE_URL = 'http://127.0.0.1:8000'


@pytest.fixture(scope='module')
def get_jwt_token():
    # Endpoint to get JWT token
    url = f"{BASE_URL}/api/token/"
    # Body with login credentials
    payload = {'username': 'admin', 'password': 'password'}
    # Headers for content type
    headers = {'Content-Type': 'application/json'}

    # Send POST request to get the token
    response = requests.post(url, json=payload, headers=headers)

    # Check if the response is successful and contains the access token
    assert response.status_code == 200, "Failed to get JWT token"
    return response.json().get('access')


def test_create_stock(get_jwt_token):
    url = f"{BASE_URL}/api/stocks/"
    headers = {'Authorization': f'Bearer {get_jwt_token}', 'Content-Type': 'application/json'}
    payload = {'name': 'Test Stock', 'price': '100.00'}
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 201
    print('Create stock:', response.json())


def test_get_stocks(get_jwt_token):
    url = f"{BASE_URL}/api/stocks/"
    headers = {'Authorization': f'Bearer {get_jwt_token}'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    print('Get stocks:', response.json())


def test_create_order(get_jwt_token):
    url = f"{BASE_URL}/api/orders/"
    headers = {'Authorization': f'Bearer {get_jwt_token}', 'Content-Type': 'application/json'}
    # Assuming stock ID 1 exists
    payload = {'stock': 1, 'trade_type': 'buy', 'quantity': 10, 'user': 1}
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 201
    print('Create order:', response.json())


def test_get_orders(get_jwt_token):
    url = f"{BASE_URL}/api/orders/"
    headers = {'Authorization': f'Bearer {get_jwt_token}'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    print('Get orders:', response.json())


def test_user_stock_value(get_jwt_token):
    stock_id = 1  # Adjust based on actual data
    url = f"{BASE_URL}/api/user_stocks/{stock_id}/"
    headers = {'Authorization': f'Bearer {get_jwt_token}'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    print('User stock value:', response.json())


def test_place_trades_in_bulk(get_jwt_token):
    url = f"{BASE_URL}/api/place_trades_in_bulk/"
    headers = {'Authorization': f'Bearer {get_jwt_token}', 'Content-Type': 'application/json'}
    payload = [
        {'stock_id': 1, 'quantity': 10, 'trade_type': 'buy'},
        {'stock_id': 2, 'quantity': 5, 'trade_type': 'sell'}
    ]
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200
    print('Place trades in bulk:', response.json())
