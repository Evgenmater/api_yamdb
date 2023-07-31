from django_filters import rest_framework as rest_filters

from reviews.models import Title


class TitleFilter(rest_filters.FilterSet):
    """Фильтрация по полю с использованием параметра 'slug'."""

    genre = rest_filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains',
    )
    category = rest_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains',
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category')
