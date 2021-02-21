from django.urls import path, include
from .views import *

app_name = 'auth'

urlpatterns = [
    path('', index_view),
    path('signin/', signin_view, name="login"),
]
