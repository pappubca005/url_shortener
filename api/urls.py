# shortener/urls.py
from django.urls import path
from .views import create_short_url, redirect_to_original

urlpatterns = [
    path('shorten/', create_short_url, name='create_short_url'),
    path('short/<str:short_code>/', redirect_to_original, name='redirect_to_original'),
]
