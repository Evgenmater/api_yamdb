"""Serializers for API YAMDB."""
from rest_framework import serializers

from .models import (
    Review, Comment, Category,
    Title, Genre, GenreTitle, User,
)


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
    """Сериализатор отзывов."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    title = serializers.SlugRelatedField(
        slug_field='name', read_only=True)

    def validate(self, data):
        title = self.context.get('title')
        request = self.context.get('request')
        if (request.method == 'POST'
           and Review.objects.filter(author=request.user, title=title
                                     ).exists()):
            raise serializers.ValidationError(
                'Вы уже написали отзыв к этому произведению.')
        return data

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Оценка производится по десятибалльной шкале.')

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')


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
    """Сериализатор комментариев."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    review = serializers.SlugRelatedField(
        slug_field='text', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date')


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
