from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('genre/<slug:slug>/', views.GenreBookListView.as_view(), name='genres'),
    path('author/<slug:slug>/', views.AuthorBookListView.as_view(), name='authors'),
    path('year/<int:year>/', views.YearBookListView.as_view(), name='years'),
    path('book/<slug:slug>/', views.SingleBookView.as_view(), name='book_detail'),
    path('book/<slug:slug>/add_comment/', views.add_comment, name='add_comment'),
    path('search/', views.BookSearchView.as_view(), name='search'),
    path('git-upd/', views.git_update, name='git-update'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
