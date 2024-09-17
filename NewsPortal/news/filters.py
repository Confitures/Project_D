from django.forms.widgets import DateTimeInput
from django_filters import (
    FilterSet,
    DateTimeFilter,
    CharFilter,
    ChoiceFilter,
    ModelChoiceFilter,
    ModelMultipleChoiceFilter,
)

from .models import Post, PostCategory, Category


class NewsFilter(FilterSet):
    created_after = DateTimeFilter(
        field_name='time_created',
        lookup_expr='gt',
        label='Дата',
        widget=DateTimeInput(
            # format='%Y-%m-%dT%H:%M',  #  не меняет результат. Почему?
            attrs={'type': 'date'},
        ),
    )

    category = ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Категория',
    )

    class Meta:
        model = Post
        fields = {
            'category': ['exact', ],
            'title': ['icontains'],
        }
