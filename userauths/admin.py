# Importing required modules from Django
from django.contrib import admin
from userauths.models import User  # Importing the custom User model

# Register your models here.

# Admin class for the User model
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']  # Specifies fields to display in the list view of the admin interface

# Registering the User model with its respective admin class
admin.site.register(User, UserAdmin)


# The custom admin class UserAdmin is defined to customize the admin interface for the User model.
# The list_display attribute specifies which fields to display in the list view of the admin interface.
# The admin.site.register() method is used to associate the User model with its admin class, allowing it to be managed via the Django admin interface.