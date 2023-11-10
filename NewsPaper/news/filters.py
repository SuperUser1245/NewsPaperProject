import django_filters
from django.forms import DateTimeInput
from django_filters import DateTimeFilter
from .models import Post


class PostFilter(django_filters.FilterSet):
    post_time = DateTimeFilter(
        field_name='post_time',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )
    class Meta:
        model = Post

        fields = {
            'post_title': ['icontains'],
            'categories': ['exact']
        }



