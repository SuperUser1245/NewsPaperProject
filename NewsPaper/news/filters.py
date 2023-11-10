import django_filters
from django.forms import DateTimeInput
from django_filters import DateTimeFilter, ModelChoiceFilter
from .models import Post, Category


class PostFilter(django_filters.FilterSet):
    categories = ModelChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        label='Category',
        empty_label='Choose category'
    )

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
        }



