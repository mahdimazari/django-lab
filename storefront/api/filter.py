import django_filters
from .models import Category, Note

class NoteFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    categories = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all())
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Note
        fields = ['title', 'categories', 'created_at']