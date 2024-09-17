from django.forms.widgets import DateInput, DateTimeInput
from django_filters import (
    FilterSet,
    ModelChoiceFilter,
    ModelMultipleChoiceFilter,
    ChoiceFilter,
    DateTimeFilter,
)
from .models import Post,


class NewsFilter(FilterSet):
    created_after = DateTimeFilter(
        field_name='time_created',
        lookup_expr='gt',
        label='Дата',
        widget=DateTimeInput(
            # format='%Y-%m-%dT%H:%M',
            attrs={'type': 'date'},
        ),
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'postcategory__category': ['exact'],
        }


