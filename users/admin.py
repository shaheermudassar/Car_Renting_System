from django.contrib import admin
from users.models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['profile_image', 'full_name']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['profile', 'address', 'town_or_area', 'city', 'country']

class LicenseDetailAdmin(admin.ModelAdmin):
    list_display = ['user', 'valid', 'expiry_date', 'license_name']

class SavedCarsAdmin(admin.ModelAdmin):
    list_display = ['user', 'car']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'created_at']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(LicenseDetail, LicenseDetailAdmin)
admin.site.register(Saved_Car, SavedCarsAdmin)
admin.site.register(Notification, NotificationAdmin)