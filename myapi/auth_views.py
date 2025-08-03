from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import BookSerializer, AuthorSerializer, GenreSerializer, YearSerializer, RegistrationSerializer
from cart.models import Cart


# Create your views here.


class RegistrationAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Создаём или получаем токен
            token, _ = Token.objects.get_or_create(user=user)

            # Создаём корзину, если её ещё нет
            Cart.objects.get_or_create(user=user)

            return Response({'token': token.key}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthStatuAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        is_authenticated = request.user.is_authenticated
        username = request.user.username
        print(is_authenticated)
        print(username)
        return Response({'is_authenticated': is_authenticated, 'username': username})
