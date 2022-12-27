from django_filters import rest_framework as rf

from reviews.models import Title


class TitleFilter(rf.FilterSet):
    """Фильтрация произведений по полям вложенных моделей."""
    name = rf.CharFilter(field_name='name', lookup_expr='icontains')
    category = rf.CharFilter(field_name='category__slug',
                             lookup_expr='icontains')
    genre = rf.CharFilter(field_name='genre__slug', lookup_expr='icontains')
    year = rf.NumberFilter(field_name='year', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
