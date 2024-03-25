from django.contrib import admin
from cars.models import *

class SpecificationInline(admin.StackedInline):
    model = Specification

class FeaturesInline(admin.StackedInline):
    model = Features

class CarImagesAdmin(admin.TabularInline):
    model = CarImages
    max_num = 4

class CarAdmin(admin.ModelAdmin):
    inlines = [CarImagesAdmin, SpecificationInline, FeaturesInline]
    list_display = ['car_image', 'name', 'model', 'brand', 'category', 'per_day_rent', 'rented', 'color', 'year_of_manufacture']
    list_filter = ['name', 'model', 'brand', 'color', 'per_day_rent', 'rented']
    list_editable = ['rented']
    search_fields = ['name']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_image']
    list_filter = ['name']

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_image']
    list_filter = ['name']

class TransmissionAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']

class FuelTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'rating', 'review']
    list_filter = ['user', 'car', 'rating']

admin.site.register(Car, CarAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Transmission, TransmissionAdmin)
admin.site.register(Fuel_Type, FuelTypeAdmin)
admin.site.register(Review, ReviewAdmin)
