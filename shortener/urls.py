from django.urls import path
from .views import home, redirect_url
from .views import home, redirect_url, URLCreateAPIView , dashboard   
from .views import URLCreateAPIView, URLRetrieveAPIView, create_short_url,redirect_to_original

print("Loading shortener.urls")  # Add this line at the top of your shortener/urls.py

urlpatterns = [
    path('', home, name='home'),
    path('<str:short_code>/', redirect_url, name='redirect_url'),
    path('api/shorten/', URLCreateAPIView.as_view(), name='url-create'),
    #path('api/shorten/<str:short_code>/', URLRetrieveAPIView.as_view(), name='url-retrieve'),  # This must be present
    path('short/<str:short_code>/', URLRetrieveAPIView.as_view(), name='url-retrieve'),  # This should handle redirects
    path('dashboard/', dashboard, name='dashboard'),
    path('short1/', create_short_url, name='create_short_url1'),
    path('short1/<str:short_code>/', redirect_to_original, name='redirect_to_original'),


]

