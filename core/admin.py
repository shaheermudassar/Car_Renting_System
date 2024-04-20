from django.contrib import admin
from core.models import Customization

class CustomizationAdmin(admin.ModelAdmin):
    list_display = ["title"]  # Display the title in the admin list view

    def has_add_permission(self, *args, **kwargs):
        return not Customization.objects.exists()  # Allow adding only if no Customization objects exist

admin.site.register(Customization, CustomizationAdmin)  # Register the Customization model with the CustomizationAdmin
