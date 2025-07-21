from rest_framework import viewsets

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
