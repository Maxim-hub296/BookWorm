from rest_framework import serializers

from shop.models import *


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
