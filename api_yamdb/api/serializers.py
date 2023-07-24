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

        pass


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre."""

    class Meta:
        model = Genre

        pass


class GenreTitleSerializer(serializers.ModelSerializer):
    """Serializer for GenreTitle."""

    class Meta:
        model = GenreTitle

        pass


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment."""

    class Meta:
        model = Comment

        pass


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for Title."""

    class Meta:
        model = Title

        pass
