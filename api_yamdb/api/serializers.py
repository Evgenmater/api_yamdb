"""Serializers for API YAMDB."""
from rest_framework import serializers

from reviews.models import Review, Comment, Category, Title, Genre, GenreTitle


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review."""
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
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    review = serializers.SlugRelatedField(
        slug_field='text', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date')


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for Title."""

    class Meta:
        model = Title

        pass
