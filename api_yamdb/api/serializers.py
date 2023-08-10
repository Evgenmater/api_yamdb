from rest_framework import serializers

from reviews.models import Comment, Category, Genre, Review, Title
from users.models import User


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор данных для JWT-Token."""

    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=200, required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор данных о пользователях."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор данных для регистрации пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email',)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    title = serializers.SlugRelatedField(
        slug_field='name', read_only=True)

    def validate(self, data):
        title_id = self.context.get('view').kwargs.get('title_id')
        request = self.context.get('request')
        if (request.method == 'POST' and Review.objects.filter(
            author=request.user,
            title=title_id,
        ).exists()):
            raise serializers.ValidationError(
                'Вы уже написали отзыв к этому произведению.')
        return data

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Оценка производится по десятибалльной шкале.')
        return value

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""
    lookup_field = 'slug'

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""
    lookup_field = 'slug'

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySlug(serializers.SlugRelatedField):
    """Сериализатор для поля категории."""
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class GenreSlug(serializers.SlugRelatedField):
    """Сериализатор для поля жанров."""
    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    review = serializers.SlugRelatedField(
        slug_field='text', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date')


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения произведений пользователями."""

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


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    category = CategorySlug(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = GenreSlug(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        read_only_fields = ('id',)
