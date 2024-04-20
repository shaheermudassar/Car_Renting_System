from django.contrib import admin  # Importing the admin module from Django
from .models import Rent, Rented_Car, Extended_Rent  # Importing the Rent, Rented_Car, and Extended_Rent models from the current directory

class RentAdmin(admin.ModelAdmin):  # Creating an admin class for the Rent model
    list_display = ["rid", "user", "car", "paid", "is_deleted", "cancelled"]  # Configuring the fields to display in the admin list view

class ExtendedRentAdmin(admin.ModelAdmin):  # Creating an admin class for the Extended_Rent model
    list_display = ["period", "number_of_period"]  # Configuring the fields to display in the admin list view

class RentedCarAdmin(admin.ModelAdmin):  # Creating an admin class for the Rented_Car model
    list_display = ["rent", "return_status", "created_at", "last_date", "over_due_charges"]  # Configuring the fields to display in the admin list view
    list_filter = ["rent", "over_due_charges"]  # Adding filters to the admin list view
    date_hierarchy = "created_at"  # Setting the date hierarchy for the admin list view

admin.site.register(Rent, RentAdmin)  # Registering the Rent model with its admin class
admin.site.register(Extended_Rent, ExtendedRentAdmin)  # Registering the Extended_Rent model with its admin class
admin.site.register(Rented_Car, RentedCarAdmin)  # Registering the Rented_Car model with its admin class
