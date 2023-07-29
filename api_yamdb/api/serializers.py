"""Serializers for API YAMDB."""
from rest_framework import serializers

from reviews.models import Review, Comment, Category, Title, Genre


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


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    """Serializer to read Titles for users."""
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        """Meta ReadOnlyTitleSerializer."""
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class TitleSerializer(serializers.ModelSerializer):
    """Serializer to add Titles."""
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        """Meta TitleSerializer."""
        model = Title
        fields = '__all__'
