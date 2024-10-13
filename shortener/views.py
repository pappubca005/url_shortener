from django.shortcuts import render, redirect, get_object_or_404
import random
import string
from .models import URL
from django.http import HttpResponse
from .forms import URLForm
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import URLSerializer
from rest_framework.decorators import api_view

def dashboard(request):
    urls = URL.objects.all()
    return render(request, 'shortener/dashboard.html', {'urls': urls})

class URLCreateAPIView(generics.CreateAPIView):
    queryset = URL.objects.all()
    serializer_class = URLSerializer
    lookup_field = 'short_code'

    def generate_short_code(self, length=6):
        characters = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choice(characters) for _ in range(length))
            if not URL.objects.filter(short_code=short_code).exists():
                return short_code

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            url_instance = serializer.save()
            url_instance.short_code = self.generate_short_code()  # Generate the short code
            url_instance.save()  # Save the short code to the database
            
            short_url = request.build_absolute_uri(f"/short/{url_instance.short_code}/")  # Correct short URL construction
            return Response({'short_url': short_url}, status=status.HTTP_201_CREATED)  # Return short URL
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_short_url(request):
    serializer = URLSerializer(data=request.data)
    if serializer.is_valid():
        url_instance = serializer.save()
        short_url = request.build_absolute_uri(f"/short/{url_instance.short_code}/")
        return Response({'short_url': short_url}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def redirect_to_original(request, short_code):
    try:
        url_instance = URL.objects.get(short_code=short_code)
        return Response({'original_url': url_instance.original_url}, status=status.HTTP_302_FOUND)
    except URL.DoesNotExist:
        return Response({'error': 'URL not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
class URLRetrieveAPIView(generics.RetrieveAPIView):
    queryset = URL.objects.all()
    lookup_field = 'short_code'  # Ensure this matches your URL pattern

    def get(self, request, short_code, *args, **kwargs):
        url_instance = get_object_or_404(URL, short_code=short_code)
        return redirect(url_instance.original_url)  # Redirect to the original URL

def home(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url_instance = form.save()
            return render(request, 'shortener/home.html', {'short_url': request.build_absolute_uri(url_instance.short_code)})
    else:
        form = URLForm()
    return render(request, 'shortener/home.html', {'form': form})

def redirect_url(request, short_code):
    try:
        url_instance = URL.objects.get(short_code=short_code)
        url_instance.click_count += 1  # Ensure this field exists in your model
        url_instance.save()
        return redirect(url_instance.original_url)
    except URL.DoesNotExist:
        return render(request, 'shortener/404.html', status=404)  # Custom 404 page
