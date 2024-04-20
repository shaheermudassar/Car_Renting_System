from django.contrib import admin
from .models import Rent, Rented_Car, Extended_Rent

class RentAdmin(admin.ModelAdmin):
    list_display = ["rid", "user", "car", "paid", "is_deleted", "cancelled"]

class ExtendedRentAdmin(admin.ModelAdmin):
    list_display = ["period", "number_of_period"]

class RentedCarAdmin(admin.ModelAdmin):
    list_display = ["rent", "return_status", "created_at", "last_date", "over_due_charges"]
    list_filter = ["rent", "over_due_charges"]
    date_hierarchy = "created_at"

admin.site.register(Rent, RentAdmin)
admin.site.register(Extended_Rent, ExtendedRentAdmin)
admin.site.register(Rented_Car, RentedCarAdmin)