from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart
from .serializers import CartSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from shop.models import Book


class CartDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Cart.objects.get(user=self.request.user)


class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        book_id = request.data.get("book_id")
        quantity = request.data.get('quantity')

        if not book_id or not quantity:
            return Response({"error": "book_id и quantity обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        book = get_object_or_404(Book, pk=book_id)
        cart = Cart.objects.get(user=request.user)
        cart.add_item(book, quantity)

        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class RemoveFromCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        book_id = request.data.get('book_id')

        cart = Cart.objects.get(user=request.user)
        book = get_object_or_404(Book, pk=book_id)

        cart.remove_item(book)

        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class UpdateCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        book_id = request.data.get("book_id")
        action = request.data.get("action")

        if not book_id or not action:
            return Response({"error": "book_id и action обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart.objects.get(user=request.user)
        book = get_object_or_404(Book, pk=book_id)
        cart_item = get_object_or_404(CartItem, cart=cart, book=book)

        if action == "increase" and cart_item.quantity < 99:
            cart_item.quantity += 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            return Response({"error": "Некорректное действие или количество вне допустимого диапазона"},
                            status=status.HTTP_400_BAD_REQUEST)

        cart_item.save()

        return Response({
            "new_quantity": cart_item.quantity,
            "item_total": cart_item.get_book_sum(),
            "cart_total": cart.get_sum(),
            "items_total": cart.get_count_of_items()
        }, status=status.HTTP_200_OK)
