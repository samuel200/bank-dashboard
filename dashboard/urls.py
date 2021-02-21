from django.urls import path, include
from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('', index_view, name="index"),
    path('transactions/', transactions_view, name="transactions"),
    path('savings/', savings_view, name="savings"),
    path('send_funds/', send_funds_view, name="send_funds"),
    path('loans/', loans_view, name="loans"),
    path('customer_support/', customer_support_view, name="customer_support"),
    path('logout/', logout_view, name="logout"),
]
