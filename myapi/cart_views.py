from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from shop.models import Book
from cart.models import Cart

class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        book_id = request.data.get('book_id')
        quantity = request.data.get("quantity")

        if not book_id or not quantity:
            return Response({"error": "book_id и quantity обязательны"},
                            status=status.HTTP_400_BAD_REQUEST)

        book = get_object_or_404(Book, pk=book_id)
        cart = Cart.objects.get(user=request.user)
        cart.add_item(book, quantity)

        return JsonResponse({"status": "ok"})

class RemoveFromCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        book_id = request.data.get('book_id')
        cart = Cart.objects.get(user=request.user)
        book = get_object_or_404(Book, pk=book_id)
        cart.remove_item(book)

        return JsonResponse({'status': 'ok'})
