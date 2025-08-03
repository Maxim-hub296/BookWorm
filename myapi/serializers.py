from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from cart.models import CartItem, Cart
from shop.models import *
from django.db import IntegrityError

User = get_user_model()


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('name', 'slug')


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['user', 'content']


class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'book']  # user добавим вручную в view

    def create(self, validated_data):
        user = self.context['request'].user
        return Comment.objects.create(user=user, **validated_data)


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    comments = CommentSerializer(source='comment_set', many=True, read_only=True)
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', "authors", 'description', 'year', 'price', 'genres', 'slug', 'image', 'comments')


class YearSerializer(serializers.Serializer):
    year = serializers.IntegerField()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data)
            Token.objects.create(user=user)  # Создаём токен
            return user
        except IntegrityError:
            raise serializers.ValidationError({
                "username": "Пользователь с таким именем уже существует."
            })


class CartItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id',
            'book',
            'quantity',
            'total_price',
        ]

    def get_total_price(self, obj):
        return obj.get_book_sum()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_sum = serializers.SerializerMethodField()
    total_count = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id',
            'items',
            'total_count',
            'total_sum'
        ]

    def get_total_sum(self, obj):
        return obj.get_sum()

    def get_total_count(self, obj):
        return obj.get_count_of_items()
