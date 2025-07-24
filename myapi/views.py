
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import generics
from django.db.models import Q
from .serializers import BookSerializer, AuthorSerializer, GenreSerializer, YearSerializer
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
