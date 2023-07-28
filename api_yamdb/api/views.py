"""ViewSets for API YAMDB."""
from django.db.models import Avg
from rest_framework import filters, viewsets

from reviews.models import Category, Genre, Title
from .mixins import ListCreateDestroyViewSet
from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          ReadOnlyTitleSerializer)


class GenreViewSet(ListCreateDestroyViewSet):
    """ViewSet for Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class CategoryViewSet(ListCreateDestroyViewSet):
    """ViewSet for Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet for Title."""
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    ).order_by("name")
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleSerializer
        return TitleSerializer
