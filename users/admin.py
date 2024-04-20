# Importing the admin module from Django
from django.contrib import admin
# Importing models from the users app
from users.models import *

# Registering models with corresponding admin classes

# Admin class for UserProfile model
class UserProfileAdmin(admin.ModelAdmin):
    # Specifies the fields to be displayed in the list view of UserProfile model
    list_display = ['profile_image', 'full_name']

# Admin class for Address model
class AddressAdmin(admin.ModelAdmin):
    # Specifies the fields to be displayed in the list view of Address model
    list_display = ['profile', 'address', 'town_or_area', 'city', 'country']

# Admin class for LicenseDetail model
class LicenseDetailAdmin(admin.ModelAdmin):
    # Specifies the fields to be displayed in the list view of LicenseDetail model
    list_display = ['user', 'valid', 'expiry_date', 'license_name']

# Admin class for Saved_Car model
class SavedCarsAdmin(admin.ModelAdmin):
    # Specifies the fields to be displayed in the list view of Saved_Car model
    list_display = ['user', 'car']

# Admin class for Notification model
class NotificationAdmin(admin.ModelAdmin):
    # Specifies the fields to be displayed in the list view of Notification model
    list_display = ['user', 'subject', 'created_at']

# Registering the admin classes with the respective models
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(LicenseDetail, LicenseDetailAdmin)
admin.site.register(Saved_Car, SavedCarsAdmin)
admin.site.register(Notification, NotificationAdmin)
