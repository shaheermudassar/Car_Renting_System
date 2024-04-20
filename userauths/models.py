# Importing required modules from Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Defining a custom user model inheriting from AbstractUser
class User(AbstractUser):
    email = models.EmailField(unique=True)  # Email field for the user, ensuring uniqueness
    username = models.CharField(max_length=100)  # Username field for the user
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # Profile image field, allowing blank and null values
    USERNAME_FIELD = "email"  # Specifies the email field as the unique identifier for authentication
    REQUIRED_FIELDS = ["username"]  # Specifies fields required for user creation other than username and password

    def __str__(self):
        return self.username  # String representation of the user object

    class Meta(AbstractUser.Meta):
        verbose_name_plural = "Users"  # Plural name for the model in the admin interface

# The custom user model User is defined inheriting from AbstractUser, providing all the built-in fields and functionalities of Django's default user model.
# Additional fields like email and profile_image are added to the user model.
# The USERNAME_FIELD attribute specifies the field used for authentication (in this case, the email).
# The REQUIRED_FIELDS attribute specifies fields required for user creation other than the default ones (username and password).
# The __str__ method is overridden to return the username as the string representation of the user object.
# The Meta inner class is used to customize the behavior of the model, such as specifying the plural name for the model in the admin interface.