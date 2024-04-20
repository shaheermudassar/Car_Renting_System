import django_filters
from cars.models import Car, Brand
from django import forms
from datetime import datetime
from django.db.models import Q

class CarFilter(django_filters.FilterSet):
    name_first = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='',
        widget=forms.TextInput(attrs={
            'class': 'rounded-lg lg:rounded-r-[200rem] lg:rounded-l-full text-[black] input input-bordered min-w-full',
            'placeholder': "Search By Name"
        })
    )

    # Second instance of the filter field
    name_second = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='',
        widget=forms.TextInput(attrs={
            'class': 'text-[black] input input-bordered min-w-full',
            'placeholder': "Search In Cars"
        })
    )
    color_choices = Car.objects.values_list('color', 'color').distinct()
    color = django_filters.ChoiceFilter(
        choices=[('', 'All Colors')] + list(color_choices),
        label='',
        empty_label='All Colors',
        widget=forms.Select(attrs={
            'class': 'text-[#b3b1ae] min-w-full select select-bordered',
        })
    )
    brand = django_filters.ModelChoiceFilter(
        queryset=Brand.objects.all(),
        label='',
        empty_label='All Brands',  # Optional, sets a default empty label
        widget=forms.Select(attrs={
            'class': 'text-[#b3b1ae] min-w-full select select-bordered',  # Add Tailwind or custom classes here
        })
    )
    current_year = datetime.now().year
    YEAR_CHOICES = [(year, str(year)) for year in range(1980, current_year + 1)]

    year_of_manufacture = django_filters.ChoiceFilter(
        choices=YEAR_CHOICES,
        label='',
        empty_label = 'All Models',
        widget=forms.Select(attrs={
            'class': 'text-[#b3b1ae] min-w-full select select-bordered',  # Add Tailwind or custom classes here
        })
    )
    
    class Meta:
        model = Car
        fields = []


