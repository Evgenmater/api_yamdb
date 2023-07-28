from rest_framework import serializers

from reviews.models import (
    Review, Comment, Category, Title, Genre, GenreTitle
)
from users.models import User


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор данных для JWT-Token."""

    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=200, required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)


class UserSerializer(serializers.ModelSerializer):
    """Сериализация данных о пользователях."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализация данных для регистрации пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email',)


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
