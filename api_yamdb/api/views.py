"""ViewSets for API YAMDB."""

from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .permissions import IsAuthorModeratorAdminOrReadOnly

from .serializers import CommentSerializer, ReviewSerializer
from reviews.models import Review, Title


class CommentViewSet(viewsets.ModelViewSet):
    """Получить список комментариев.
    Добавить новый комментарий к отзыву.
    Получить комментарий по id.
    Обновить комментарий по id.
    Удалить комментарий."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_review(self):
        review = get_object_or_404(
            Review,
            title_id=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id'),)
        return review

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Получить список отзывов.
    Добавить новый отзыв.
    Получить отзыв по id.
    Обновить отзыв по id.
    """

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
