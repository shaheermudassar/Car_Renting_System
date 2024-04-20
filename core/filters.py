import django_filters  # Import the django_filters module for creating filters
from cars.models import Car, Brand  # Import the Car and Brand models
from django import forms  # Import forms module from Django for form-related functionality
from datetime import datetime  # Import datetime module to work with dates
from django.db.models import Q  # Import Q object for complex queries

class CarFilter(django_filters.FilterSet):
    # Filter for searching cars by name
    name_first = django_filters.CharFilter(
        field_name='name',  # Field name to filter on
        lookup_expr='icontains',  # Case-insensitive containment lookup
        label='',  # Empty label, as it's a placeholder
        widget=forms.TextInput(attrs={  # Widget for the HTML input element
            'class': 'rounded-lg lg:rounded-r-[200rem] lg:rounded-l-full text-[black] input input-bordered min-w-full',  # CSS classes for styling
            'placeholder': "Search By Name"  # Placeholder text for the input
        })
    )

    # Second instance of the filter field
    name_second = django_filters.CharFilter(
        field_name='name',  # Field name to filter on
        lookup_expr='icontains',  # Case-insensitive containment lookup
        label='',  # Empty label, as it's a placeholder
        widget=forms.TextInput(attrs={  # Widget for the HTML input element
            'class': 'text-[black] input input-bordered min-w-full',  # CSS classes for styling
            'placeholder': "Search In Cars"  # Placeholder text for the input
        })
    )

    # Choices for filtering by car color
    color_choices = Car.objects.values_list('color', 'color').distinct()
    color = django_filters.ChoiceFilter(
        choices=[('', 'All Colors')] + list(color_choices),  # Add an option for all colors
        label='',  # Empty label
        empty_label='All Colors',  # Label for the default empty choice
        widget=forms.Select(attrs={  # Widget for the HTML select element
            'class': 'text-[#b3b1ae] min-w-full select select-bordered',  # CSS classes for styling
        })
    )

    # Filter for selecting car brand
    brand = django_filters.ModelChoiceFilter(
        queryset=Brand.objects.all(),  # Queryset for available brands
        label='',  # Empty label
        empty_label='All Brands',  # Label for the default empty choice
        widget=forms.Select(attrs={  # Widget for the HTML select element
            'class': 'text-[#b3b1ae] min-w-full select select-bordered',  # CSS classes for styling
        })
    )

    # Choices for filtering by year of manufacture
    current_year = datetime.now().year  # Get the current year
    YEAR_CHOICES = [(year, str(year)) for year in range(1980, current_year + 1)]  # Generate choices for years

    year_of_manufacture = django_filters.ChoiceFilter(
        choices=YEAR_CHOICES,  # Choices for year of manufacture
        label='',  # Empty label
        empty_label='All Models',  # Label for the default empty choice
        widget=forms.Select(attrs={  # Widget for the HTML select element
            'class': 'text-[#b3b1ae] min-w-full select select-bordered',  # CSS classes for styling
        })
    )
    
    class Meta:
        model = Car  # Specify the model to filter
        fields = []  # Specify the fields to use for filtering (empty for all fields)
