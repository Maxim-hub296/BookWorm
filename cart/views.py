from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, TemplateView

from cart.models import Cart, CartItem
from shop.models import Book


class GoodByeView(TemplateView):
    template_name = 'cart/goodbye.html'


# Create your views here.
class CartView(DetailView, LoginRequiredMixin):
    model = Cart
    template_name = "cart/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cart'] = self.model.objects.get(user=self.request.user)
        return context


@login_required
def add_to_cart(request):
    if request.method == "POST":
        book_id = request.POST["book_id"]
        quantity = request.POST["quantity"]

        book = get_object_or_404(Book, pk=book_id)
        cart = Cart.objects.get(user=request.user)
        cart.add_item(book, quantity)

        return JsonResponse({"status": "ok"})

@login_required
def remove_from_cart(request):
    if request.method == "POST":
        book_id = request.POST["book_id"]
        cart = Cart.objects.get(user=request.user)
        book = get_object_or_404(Book, pk=book_id)
        cart.remove_item(book)

        return JsonResponse({"status": "ok"})

@login_required
def update_cart_item(request):
    if request.method == "POST":
        book_id = request.POST["book_id"]
        action = request.POST["action"]

        cart = Cart.objects.get(user=request.user)
        book = get_object_or_404(Book, pk=book_id)
        cart_item = CartItem.objects.get(cart=cart, book=book)
        if action == "increase" and cart_item.quantity < 99:
            cart_item.quantity += 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1

        cart_item.save()

        return JsonResponse({
            "new_quantity": cart_item.quantity,
            "item_total": cart_item.get_book_sum(),
            "cart_total": cart.get_sum(),
            "items_total": cart.get_count_of_items()
        })