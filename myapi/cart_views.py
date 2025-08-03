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

