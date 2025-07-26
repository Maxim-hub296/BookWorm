from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'authors', views.AuthorsViewSet)
router.register(r'genres', views.GenresViewSet)
router.register(r'years', views.YearViewSet, basename='year')


urlpatterns = [
    path('', include(router.urls)),
    path('genre/<slug:slug>/', views.GenreBookListAPIView.as_view(), name='api-genre'),
    path('author/<slug:slug>/', views.AuthorBookListAPIView.as_view(), name='api-author'),
    path('year/<int:year>/', views.YearBookListAPIView.as_view(), name='api-year'),
    path('search/', views.SearchBookListAPIView.as_view(), name='api-search'),

    path('register/', views.RegistrationAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('auth-status/', views.AuthStatuAPIView.as_view(), name='hello'),

    path('api-auth/', include('rest_framework.urls',  namespace='rest_fram'))
]