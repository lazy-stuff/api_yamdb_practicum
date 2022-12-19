import django_filters

from titles.models import Title


class TitleFilters(django_filters.FilterSet):
    """Фильтры для TitlesViewSet."""
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    year = django_filters.NumberFilter(field_name='year')
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ['name', 'year', 'genre', 'category']
