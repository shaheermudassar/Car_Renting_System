from django.db import models

class Customization(models.Model):
    title = models.CharField(max_length=220, default="Customizations", editable=False)  # Title of the customization (default is "Customizations")
    main_small_heading = models.CharField(max_length=220, default="Find Cars For Rent Near You")  # Small heading for the main screen
    main_large_heading = models.CharField(max_length=220, default="Rent Your Dream Car")  # Large heading for the main screen
    main_screen_image_desktop = models.ImageField(upload_to="Images/Main_Images_Desktop", null=True)  # Image for the main screen (desktop version)
    main_screen_image_mobile = models.ImageField(upload_to="Images/Main_Images_Mobile", null=True)  # Image for the main screen (mobile version)
    listing_image_desktop = models.ImageField(upload_to="Images/Listing_Images_desktop", null=True)  # Image for the listing page (desktop version)
    listing_image_mobile = models.ImageField(upload_to="Images/Listing_Images_mobile", null=True)  # Image for the listing page (mobile version)

    class Meta:
        verbose_name_plural = "Customizations"  # Plural name for the model

    def __str__(self):
        return self.title  # String representation of the object, returns the title
