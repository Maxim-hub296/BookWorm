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
    path('api-auth/', include('rest_framework.urls',  namespace='rest_fram'))
]