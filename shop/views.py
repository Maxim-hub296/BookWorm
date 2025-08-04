import git
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from shop.forms import AddCommentForm
from shop.models import Book, Genre, Comment, Author
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q


# Create your views here.
class Home(ListView):
    model = Book
    template_name = "shop/books.html"
    context_object_name = "book_list"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.add_random_book(context)
        self.add_sidebar_data(context)
        return context

    @staticmethod
    def add_sidebar_data(context):
        """Добавляет данные для сайдбара в контекст"""
        context['genres'] = Genre.objects.all().distinct()
        context['authors'] = Author.objects.all().distinct()
        context['years'] = Book.objects.exclude(year__isnull=True) \
            .values_list('year', flat=True) \
            .order_by('-year') \
            .distinct()
        return context

    @staticmethod
    def add_random_book(context):
        if Book.objects.exists():
            context['random_book'] = Book.objects.order_by("?").first()
        else:
            context['random_book'] = None
        return context


class GenreBookListView(ListView):
    model = Book
    template_name = 'shop/books.html'
    context_object_name = 'book_list'
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(genres__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем данные для сайдбара
        Home().add_random_book(context)
        Home().add_sidebar_data(context)
        return context


class AuthorBookListView(ListView):
    model = Book
    template_name = 'shop/books.html'
    context_object_name = 'book_list'
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(authors__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем данные для сайдбара
        Home().add_random_book(context)
        Home().add_sidebar_data(context)
        return context


class YearBookListView(ListView):
    model = Book
    template_name = 'shop/books.html'
    context_object_name = 'book_list'
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(year=self.kwargs['year'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем данные для сайдбара
        Home().add_random_book(context)
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

        if 'form' not in context:
            context['form'] = AddCommentForm
        return context


class BookSearchView(ListView):
    template_name = 'shop/books.html'
    context_object_name = 'book_list'
    paginate_by = 10
    model = Book

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')

        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(authors__name__icontains=search_query)
        ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get('q', "")
        Home().add_random_book(context)
        Home().add_sidebar_data(context)
        return context


@login_required
def add_comment(request, slug):
    book = get_object_or_404(Book, slug=slug)

    if request.method == 'POST':
        form = AddCommentForm(request.POST)

        if form.is_valid():
            # Правильное извлечение данных из формы
            content = form.cleaned_data['content']

            # Создаем и сохраняем комментарий
            comment = Comment(
                content=content,
                book=book,
                user=request.user
            )
            comment.save()

            messages.success(request, 'Комментарий успешно добавлен!')
            return redirect('shop:book_detail', slug=slug)
        else:
            # Добавляем сообщения об ошибках формы
            for error in form.errors.values():
                messages.error(request, error)

    # Всегда редиректим обратно на страницу книги
    return redirect('shop:book_detail', slug=slug)


def git_update(request):
    if request.method == 'POST':
        repo = git.Repo('https://github.com/Maxim-hub296/BookWorm')
        origin = repo.remotes.origin

        origin.pull()

        return JsonResponse({'status': 'ok'})


