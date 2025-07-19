from django.urls import path

from . import views

app_name = 'cart'
urlpatterns = [
    path('<int:pk>/', views.CartView.as_view(), name='cart'),
    path('add/', views.add_to_cart, name='add'),
    path('update/', views.update_cart_item, name='update'),
    path('delete/', views.remove_from_cart, name='delete'),
    path('goodbye/', views.GoodByeView.as_view(), name='goodbye'),

]