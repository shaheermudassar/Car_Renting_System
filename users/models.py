# Importing required modules from Django
from django.db import models
from userauths.models import User  # Importing the custom User model
from django.utils.html import mark_safe  # Helper function for generating HTML
from django.db.models.signals import post_save  # Signal for post-save events
from django.dispatch import receiver  # Decorator for signal receivers
from cars.models import Car  # Importing the Car model from the cars app

# Model for storing user profiles
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # One-to-one relationship with the User model
    first_name = models.CharField(max_length=100, null=True, blank=True)  # Field for first name
    last_name = models.CharField(max_length=100, null=True, blank=True)  # Field for last name
    contact = models.CharField(max_length=100, null=True, blank=True)  # Field for contact information
    cnic = models.CharField(max_length=100, null=True, blank=True)  # Field for CNIC (Citizen's National Identity Card)
    profile_pic = models.ImageField(upload_to='Users/Profile_pics', null=True, blank=True)  # Field for profile picture
    created_at = models.DateTimeField(auto_now_add=True)  # Field for creation timestamp

    class Meta:
        verbose_name_plural = "User_Profiles"  # Plural name for the model in the admin interface

    # Method to get the full name of the user
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    # Method to get the profile image of the user
    def profile_image(self):
        if self.profile_pic:
            return mark_safe('<img src="%s" width="50" height="50"/>' % (self.profile_pic.url))
        else:
            return self.user.username
    
    # String representation of the UserProfile object
    def __str__(self):
        if self.first_name:
            return self.first_name
        else:
            return self.user.username

# Model for storing user addresses
class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="address")  # One-to-one relationship with the User model
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # Foreign key to the UserProfile model
    country = models.CharField(max_length=100, null=True, blank=True)  # Field for country
    city = models.CharField(max_length=100, null=True, blank=True)  # Field for city
    town_or_area = models.CharField(max_length=200, null=True, blank=True)  # Field for town or area
    address = models.TextField(null=True, blank=True)  # Field for address
    created_at = models.DateTimeField(auto_now_add=True)  # Field for creation timestamp

    class Meta:
        verbose_name_plural = "Address"  # Plural name for the model in the admin interface

    # String representation of the Address object
    def __str__(self):
        return self.user.username

# Model for storing saved cars by users
class Saved_Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saves")  # Foreign key to the User model
    car = models.ForeignKey(Car, on_delete=models.CASCADE)  # Foreign key to the Car model
    class Meta:
        verbose_name_plural = "Saved Cars"  # Plural name for the model in the admin interface

    # String representation of the Saved_Car object
    def __str__(self):
        return self.user.username

# Model for storing license details of users
class LicenseDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="license")  # One-to-one relationship with the User model
    license_pic = models.ImageField(upload_to='Users/License', null=True, blank=True)  # Field for license picture
    license_name = models.CharField(max_length=100, null=True, blank=True)  # Field for license name
    expiry_date = models.DateField(null=True, blank=True)  # Field for license expiry date
    valid = models.BooleanField(default=False)  # Field for indicating whether the license is valid
    class Meta:
        verbose_name_plural = "License Details"  # Plural name for the model in the admin interface

    # String representation of the LicenseDetail object
    def __str__(self):
        return self.user.username

# Model for storing notifications for users
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")  # Foreign key to the User model
    subject = models.CharField(max_length=255, null=True)  # Field for notification subject
    body = models.TextField(null=True)  # Field for notification body
    seen = models.BooleanField(default=False)  # Field for indicating whether the notification has been seen
    created_at = models.DateTimeField(auto_now_add=True)  # Field for creation timestamp
    class Meta:
        verbose_name_plural = "Notifications"  # Plural name for the model in the admin interface

    # String representation of the Notification object
    def __str__(self):
        return self.user.username

# Signal receiver function to create user profile, address, and license detail upon user creation
@receiver(post_save, sender=User)  # Decorator to connect the function to the post_save signal of the User model
def create_user_profile(sender, instance, created, *args, **kwargs):
    """
    Signal receiver function to create user profile, address, and license detail upon user creation.

    Args:
        sender: The model class that sends the signal.
        instance: The actual instance of the model that sent the signal.
        created: A boolean value indicating whether a new instance was created.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.
    """
    # Check if a new user instance is created
    if created:
        # Check if a UserProfile object does not already exist for the user
        if not UserProfile.objects.filter(user=instance).exists():
            # Create a new UserProfile object for the user
            UserProfile.objects.create(
                user=instance,  # Assigning the user instance to the user field of UserProfile
                first_name=instance.first_name or None,  # Assigning the user's first name if available
                last_name=instance.last_name or None,  # Assigning the user's last name if available
            ),
        
        # Retrieve the UserProfile object associated with the user
        profile = UserProfile.objects.get(user=instance)
        
        # Create an Address object for the user
        Address.objects.create(user=instance, profile=profile)
        
        # Create a LicenseDetail object for the user
        LicenseDetail.objects.create(user=instance)
