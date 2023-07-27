"""Serializers for API YAMDB."""
from rest_framework import serializers

from reviews.models import Review, Comment, Category, Title, Genre, GenreTitle


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review."""

    class Meta:
        model = Review

        pass


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category."""

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre."""

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment."""

    class Meta:
        model = Comment

        pass


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for Title."""
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
