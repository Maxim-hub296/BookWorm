

from django.views.generic import ListView, DetailView

from shop.models import Book, Genre, Comment


# Create your views here.
class Home(ListView):
    model = Book
    template_name = "shop/books.html"
    context_object_name = "book_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.add_sidebar_data(context)
        return context

    def add_sidebar_data(self, context):
        """Добавляет данные для сайдбара в контекст"""
        context['genres'] = Genre.objects.all().distinct()
        context['years'] = Book.objects.exclude(year__isnull=True) \
            .values_list('year', flat=True) \
            .order_by('-year') \
            .distinct()
        context['authors'] = Book.objects.values_list('author', flat=True) \
            .order_by('author') \
            .distinct()
        return context


class GenreBookListView(ListView):
    model = Book
    template_name = 'shop/books.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        return self.model.objects.filter(genres__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем данные для сайдбара
        Home().add_sidebar_data(context)
        return context


class AuthorBookListView(ListView):
    model = Book
    template_name = 'shop/books.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        return self.model.objects.filter(author=self.kwargs['author'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем данные для сайдбара
        Home().add_sidebar_data(context)
        return context


class YearBookListView(ListView):
    model = Book
    template_name = 'shop/books.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        return self.model.objects.filter(year=self.kwargs['year'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем данные для сайдбара
        Home().add_sidebar_data(context)
        return context


class SingleBookView(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'shop/book.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(book=self.get_object())
        context['comments'] = comments
        context['genres'] = Genre.objects.filter(book=self.get_object())
        return context
