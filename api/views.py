# shortener/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import URL
from .serializers import URLSerializer

@api_view(['POST'])
def create_short_url(request):
    serializer = URLSerializer(data=request.data)
    if serializer.is_valid():
        url_instance = serializer.save()
        short_url = request.build_absolute_uri(f"/short/{url_instance.short_code}/")
        print("API generated short url")
        return Response({'short_url': short_url}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def redirect_to_original(request, short_code):
    try:
        url_instance = URL.objects.get(short_code=short_code)
        return Response({'original_url': url_instance.original_url}, status=status.HTTP_302_FOUND)
    except URL.DoesNotExist:
        return Response({'error': 'URL not found'}, status=status.HTTP_404_NOT_FOUND)
