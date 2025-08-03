from django.urls import include, path
from rest_framework import routers
from . import auth_views
from . import shop_views
from .cart_views import CartDetailAPIView, AddToCartAPIView, RemoveFromCartAPIView

router = routers.DefaultRouter()
router.register(r'books', shop_views.BookViewSet, basename='book')
router.register(r'authors', shop_views.AuthorsViewSet)
router.register(r'genres', shop_views.GenresViewSet)
router.register(r'years', shop_views.YearViewSet, basename='year')

urlpatterns = [
    path('', include(router.urls)),
    path('genre/<slug:slug>/', shop_views.GenreBookListAPIView.as_view(), name='api-genre'),
    path('author/<slug:slug>/', shop_views.AuthorBookListAPIView.as_view(), name='api-author'),
    path('year/<int:year>/', shop_views.YearBookListAPIView.as_view(), name='api-year'),
    path('search/', shop_views.SearchBookListAPIView.as_view(), name='api-search'),

    path('register/', auth_views.RegistrationAPIView.as_view(), name='register'),
    path('login/', auth_views.LoginAPIView.as_view(), name='login'),
    path('logout/', auth_views.LogoutAPIView.as_view(), name='logout'),
    path('auth-status/', auth_views.AuthStatuAPIView.as_view(), name='auth-status'),

    path('add-comment/', shop_views.AddCommentAPIView.as_view(), name='add-comment'),

    path('cart/', CartDetailAPIView.as_view(), name='cart'),
    path('cart-add/', AddToCartAPIView.as_view(), name='cart-add'),
    path('cart-remove', RemoveFromCartAPIView.as_view(), name='cart-remove'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_fram'))
]
