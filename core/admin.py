from django.contrib import admin
from core.models import Customization

class CustomizationAdmin(admin.ModelAdmin):
    list_display = ["title"]
    def has_add_permission(self, *args, **kwargs):
        return not Customization.objects.exists()

admin.site.register(Customization, CustomizationAdmin)