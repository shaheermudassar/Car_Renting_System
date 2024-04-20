# Importing required modules from Django
from django.contrib import admin
from cars.models import *  # Importing all models from the cars app

# Inline classes for CarAdmin
class SpecificationInline(admin.StackedInline):
    model = Specification  # Specifies the model for the inline

class FeaturesInline(admin.StackedInline):
    model = Features  # Specifies the model for the inline

class CarImagesAdmin(admin.TabularInline):
    model = CarImages  # Specifies the model for the inline
    max_num = 4  # Maximum number of CarImages to display

# Admin class for Car model
class CarAdmin(admin.ModelAdmin):
    inlines = [CarImagesAdmin, SpecificationInline, FeaturesInline]  # Specifies inline models
    list_display = ['car_image', 'name', 'model', 'brand', 'category', 'per_day_rent', 'rented', 'color', 'year_of_manufacture']  # Specifies fields to display in the list view
    list_filter = ['name', 'model', 'brand', 'color', 'per_day_rent', 'rented']  # Specifies fields for filtering
    list_editable = ['rented']  # Specifies editable fields in the list view
    search_fields = ['name']  # Specifies fields for search

# Admin class for Category model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_image']  # Specifies fields to display in the list view
    list_filter = ['name']  # Specifies fields for filtering

# Admin class for Brand model
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_image']  # Specifies fields to display in the list view
    list_filter = ['name']  # Specifies fields for filtering

# Admin class for Transmission model
class TransmissionAdmin(admin.ModelAdmin):
    list_display = ['name']  # Specifies fields to display in the list view
    list_filter = ['name']  # Specifies fields for filtering

# Admin class for Fuel_Type model
class FuelTypeAdmin(admin.ModelAdmin):
    list_display = ['name']  # Specifies fields to display in the list view
    list_filter = ['name']  # Specifies fields for filtering

# Admin class for Review model
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'rating', 'review']  # Specifies fields to display in the list view
    list_filter = ['user', 'car', 'rating']  # Specifies fields for filtering

# Registering models with their respective admin classes
admin.site.register(Car, CarAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Transmission, TransmissionAdmin)
admin.site.register(Fuel_Type, FuelTypeAdmin)
admin.site.register(Review, ReviewAdmin)

# Inline classes are defined for related models to be displayed within the admin interface of the Car model.
# Admin classes are defined for each model, specifying how the models should be displayed and interacted with in the admin interface.
# The register() method is used to associate each model with its corresponding admin class, allowing them to be managed via the Django admin interface.