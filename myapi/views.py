from ast import AugLoad

from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import generics
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import BookSerializer, AuthorSerializer, GenreSerializer, YearSerializer, RegistrationSerializer
from shop.models import Book, Author, Genre


# Create your views here.
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class AuthorsViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().distinct()
    serializer_class = AuthorSerializer

class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().distinct()
    serializer_class = GenreSerializer

class YearViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.values('year').distinct().order_by("-year")
    serializer_class = YearSerializer

class GenreBookListAPIView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        genre_slug = self.kwargs['slug']

        genre = get_object_or_404(Genre, slug=genre_slug)
        return Book.objects.filter(genres=genre)

class AuthorBookListAPIView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        author_slug = self.kwargs['slug']

        author = get_object_or_404(Author, slug=author_slug)
        return Book.objects.filter(authors=author)

class YearBookListAPIView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        year = self.kwargs['year']

        return Book.objects.filter(year=year)

class SearchBookListAPIView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()

        search_query = self.request.GET.get('q', '')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(authors__name__icontains=search_query)
            ).distinct()

        return queryset


class RegistrationAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = user.auth_token.key
            return Response({'token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AuthStatuAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        is_authenticated = request.user.is_authnticated
        return Response({'is_authenticated': is_authenticated})

