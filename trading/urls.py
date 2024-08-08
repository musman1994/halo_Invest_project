from django.urls import path
from .views import StockListCreateView, OrderListCreateView, UserStockValueView, LoginView, LogoutView, \
    PlaceTradesInBulk

urlpatterns = [
    path('stocks/', StockListCreateView.as_view(), name='stock_list_create'),
    path('orders/', OrderListCreateView.as_view(), name='order_list_create'),
    path('user_stocks/<int:stock_id>/', UserStockValueView.as_view(), name='user_stock_value'),
    path('place_trades_in_bulk/', PlaceTradesInBulk.as_view(), name='place_trades_in_bulk'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
