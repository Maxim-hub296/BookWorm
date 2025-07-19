from .models import Comment, Author
# Register your models here.
from django.contrib import admin
from .models import Book, Genre


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # Поля в списке
    prepopulated_fields = {'slug': ('name',)}  # Автозаполнение slug


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_genres')  # Показываем жанры в списке книг
    filter_horizontal = ('genres', "authors")  # Красивый виджет для выбора жанров
    prepopulated_fields = {'slug': ('title',)}

    # Метод для отображения жанров в списке книг
    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    display_genres.short_description = 'Жанры'

    def display_authors(self, obj):
        return ", ".join([author.name for author in obj.authors.all()])

    display_authors.short_description = 'Авторы'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('book', 'short_content')  # Добавьте created_at в модель, если нужно
    list_filter = ('book',)
    search_fields = ('content', 'book__title')

    def short_content(self, obj):
        return f"{obj.content[:50]}..." if len(obj.content) > 50 else obj.content

    short_content.short_description = 'Комментарий'


admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
